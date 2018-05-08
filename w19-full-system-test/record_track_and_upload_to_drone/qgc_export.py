import json
import numpy as np
from utm import utmconv
def parse_data(inputfile="./resources/new_log_wps.log"):
    init = False
    gps_data = np.zeros(9)
    with open(inputfile, 'r') as data_file:
        for line in data_file:
            row_data = line.rstrip().split(',')
            # Read only the lines with 9 items, and ignore headers as well.
            if len(row_data) == 4  and row_data[0][0] != "#":
                # The first time, the array has to be initialized.
                if not init:
                    gps_data = np.array(row_data)
                    init = True
                else:
                    gps_data = np.vstack((gps_data, row_data))
    # Transform the string-type data to float.
    gps_data = gps_data.astype(np.float64)
    return gps_data

class exportQDC:
    def __init__(self):
        #self.filetype = filetype
        #self.polygon = polygon
        #self.versionGF = versionGF
        #self.groundStation = groundStation
        return

    items = []
    mission = {}
    plan = {}
    geoFence = {}
    rallyPoints = {}


    def write_begin(self, filetype, polygon, versionGF, groundStation):
        self.plan['fileType'] = 'Plan'#"'" +  str(filetype) + "'"
        self.geoFence['polygon'] =  polygon # []
        self.geoFence['version'] =  versionGF
        self.plan['geoFence'] = self.geoFence
        self.plan['groundStation'] = str(groundStation)

    def write_item_data(self, auto_cnt, cmd_id, jmp_id, frm_id, params, tp):
        item = {}
        item['autoContinue'] = True
        item['command'] = cmd_id
        item['doJumpId'] = jmp_id
        item['frame'] = frm_id
        item['params'] = params
        item['type'] = tp
        self.items.append(item)

    def all_write_functions(self):
        self.write_begin()
        self.begin(self, file, fltp, poly, vers, geoF, grndStation)

    def write_mission_end(self, cruiseSpd, firmwareTp, hoverSpd, plHomePos, vehicleTp, versionMsn):
        self.mission['cruiseSpeed'] = cruiseSpd
        self.mission['firmwareType'] = firmwareTp
        self.mission['hoverSpeed'] = hoverSpd
        self.mission['items'] = self.items
        self.mission['plannedHomePosition'] = plHomePos #[55.4713, 10.3256, 50]
        self.mission['vehicleType'] = vehicleTp
        self.mission['version'] = versionMsn
        self.plan['mission'] = self.mission

    def write_rally_points(self, points, versionRl):
        self.rallyPoints['points'] = points#[]
        self.rallyPoints['version'] = versionRl
        self.plan['rallyPoints'] = self.rallyPoints

    def write_end_file(self, fname,versionPl, indnt, srtKs):
        self.plan['version'] = versionPl
        self.plan_json = json.dumps(self.plan, indent = indnt, sort_keys = srtKs)# indnt=4   True
        self.file = open(fname,'w')
        self.file.write (self.plan_json)
        self.file.close()
        #write_item_data(self, auto_cnt, cmd_id, jmp_id, frm_id, params, tp):
    def write_cycle_items(self, gps_data, auto_cnt, cmd_id, frm_id, coordB, coordE, tp):
        for i in range (coordB, coordE):   #len(gps_data)
            params =[0,0,0,0,gps_data[i][1],gps_data[i][2],15]
            self.write_item_data(True, cmd_id, i + 1, frm_id,params, tp)

#auto_cnt = true
#cmd_id = 22
#frm_id = 3
#tp = "'SimpleItem'"
#jmp_id = i

##write_item_data(auto_cnt, cmd_id, jmp_id, frm_id, tp)
def main():
    gps_data = parse_data()
    print(gps_data)
    #geo_coordinates = gps_data[:, 1:3]
    geo_coordinates = gps_data[0, 1]
    geo_coordinates = gps_data[:, 2]
   # geo_coordinates = gps_data[:, 3]
    print(geo_coordinates)
    export = exportQDC()
    export.write_begin('Plan', [], 1, 'QGroundControl')
    export.write_cycle_items(gps_data, True, 22, 3, 0, 1, 'SimpleItem')
    export.write_cycle_items(gps_data, True, 16, 3, 1, len(gps_data), 'SimpleItem')
    export.write_mission_end(15, 3, 5, [55.4713, 10.3256, 50], 2, 2)
    export.write_rally_points([], 1)
    export.write_end_file('missionZZZ.plan',1, 14 , True)
    print(export.plan)

if __name__ == "__main__":
    gps_data = main()

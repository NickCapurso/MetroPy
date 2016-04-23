import requests, json
import MetroConstants as Constants
from MetroData import Line,Station
from time import sleep

class MetroInterface:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def getLineInfos(self):
        jsonResp = json.loads(requests.get(Constants.URL_LINES_LIST + "?api_key=" +self.apiKey).text)
        lineInfos = {}
        for i in jsonResp[Constants.LINES_TOP]:
            displayName = i[Constants.LINES_DISPLAY_NAME]
            lineCode = i[Constants.LINES_LINE_CODE]
            startCode = i[Constants.LINES_START_CODE]
            endCode = i[Constants.LINES_END_CODE]
            lineInfos[lineCode] = Line(displayName, lineCode, startCode, endCode)
        return lineInfos

    def getStationInfos(self):
        jsonResp = json.loads(requests.get(Constants.URL_STATION_LIST + "?api_key=" +self.apiKey).text)
        stationInfos = {}
        for i in jsonResp[Constants.STATION_LIST_TOP]:
            name = i[Constants.STATION_LIST_NAME]
            code = i[Constants.STATION_LIST_CODE]
            lc1 = i[Constants.STATION_LIST_LC1]
            lc2 = i[Constants.STATION_LIST_LC2]
            lc3 = i[Constants.STATION_LIST_LC3]
            lc4 = i[Constants.STATION_LIST_LC4]
            st1 = i[Constants.STATION_LIST_ST1]
            st2 = i[Constants.STATION_LIST_ST2]

            if name not in stationInfos:
                station = Station(name, code, lc1, lc2, lc3, lc4, st1, st2)
                stationInfos[name] = station
                stationInfos[code] = station

                for st in [st1, st2]:
                    if st:
                        stationInfos[st] = station
            else:
                station = stationInfos[name]
                for newLine in [lc1, lc2, lc3, lc4]:
                    if newLine:
                        station.addLine(newLine)
                for newCode in [st1, st2, code]:
                    if newCode:
                        station.addStation(newCode)
                        if newCode not in stationInfos:
                            stationInfos[newCode] = station
        return stationInfos


    def getLineAvgSpeed(self, lineCode, startCode, endCode):
        jsonResp = json.loads(requests.get(Constants.URL_STATION_STATION_INFO+ "?FromStationCode=" + startCode + "&ToStationCode=" + endCode + "&api_key=" +self.apiKey).text)
       
        info = jsonResp[Constants.STATION_STATION_TOP][0]
        totalMiles = info[Constants.STATION_STATION_MILES]
        time = info[Constants.STATION_STATION_TIME]
        return totalMiles * 60 / time


    def getOrderedStationList(self, lineCode, startCode, endCode):
        jsonResp = json.loads(requests.get(Constants.URL_STATION_PATH + "?FromStationCode=" + startCode + "&ToStationCode=" + endCode + "&api_key=" +self.apiKey).text)

        orderedStations = []
        for i in jsonResp[Constants.STATION_PATH_TOP]:
            orderedStations.append(i[Constants.STATION_PATH_CODE])

        return orderedStations


    def getDistancesToGoal(self, destCode):
        jsonResp = json.loads(requests.get(Constants.URL_STATION_STATION_INFO + "?ToStationCode=" + destCode + "&api_key=" +self.apiKey).text)
        stationDists = {}

        for i in jsonResp[Constants.STATION_STATION_TOP]:
            sourceStation = i[Constants.STATION_STATION_SOURCE]
            stationDists[sourceStation] = i[Constants.STATION_STATION_MILES]
        stationDists[destCode] = 0
        return stationDists


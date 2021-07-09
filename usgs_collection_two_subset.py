import pandas as pd
import os


def getUSGSCollTwoMetadata(csvFile, path, row, tier, cloud, timeFrom, timeTo, previous, missionName):
    print("\nReading raw USGS csv file...\n")
    with open(csvFile) as f:
        fileEncoding = f.encoding
        all_scenes = pd.read_csv(csvFile, encoding=fileEncoding, parse_dates=[
            'Date Acquired'], index_col=['Date Acquired'])
        print("Image entries in raw dataset:", all_scenes.shape[0], "\n")

    # subset images by location
    wrs_path = path  # Landsat paths
    wrs_row = row  # Landsat rows
    loc_scenes = all_scenes[all_scenes['WRS Path'].isin(wrs_path) &
                            all_scenes['WRS Row'].isin(wrs_row)]
    print("Location-specific images:", loc_scenes.shape[0], "\n")

    # subset images by tier
    loc_scenes = loc_scenes[loc_scenes['Collection Category'] == tier]
    print("Tier", tier[1], "images: ", loc_scenes.shape[0], "\n")

    # subset images by cloud cover
    loc_scenes = loc_scenes[loc_scenes['Land Cloud Cover'] <= cloud]
    print("Cloud Cover condition applied. Remaining images:",
          loc_scenes.shape[0], "\n")

    # subset images by date
    loc_scenes = loc_scenes[timeFrom:timeTo]
    print("Images between", timeFrom, "and",
          timeTo + ":", loc_scenes.shape[0], "\n")

    # select displayID column
    displayID = loc_scenes['Display ID']

    # select header for output text file (as requested by USGS)
    missionID = missionName
    if missionID == "TML1":
        missionHeader = "landsat_tm_c2_l1|displayId"
    elif missionID == "TML2":
        missionHeader = "landsat_tm_c2_l2|displayId"
    elif missionID == "ETML1":
        missionHeader = "landsat_etm_c2_l1|displayId"
    elif missionID == "ETML2":
        missionHeader = "landsat_etm_c2_l2|displayId"
    elif missionID == "L8L1":
        missionHeader = "landsat_ot_c2_l1|displayId"
    elif missionID == "L8L2":
        missionHeader = "landsat_ot_c2_l2|displayId"

    # set file names
    fileNameOne = "temp_%s.txt" % missionHeader[:-10]
    fileNameTwo = "scenes_%s.txt" % missionHeader[:-10]

    # open last scene ID list if given
    if previous != None:
        print("Eliminated repeated images.\n")
        # open given file with previous scene IDs
        with open(previous) as f:
            fileEncoding = f.encoding
            lastDisplayID = pd.read_csv(
                previous, encoding=fileEncoding)
        # remove repeated scene IDs
        uniqueDisplayID = loc_scenes['Display ID'][~loc_scenes['Display ID'].isin(
            lastDisplayID[missionHeader])].drop_duplicates()
        print("Final image count:", uniqueDisplayID.shape[0], "\n")
        # save scene ID values in a text file (one per line)
        uniqueDisplayID.to_csv(fileNameOne,
                               header=False, index=False, sep='\n')
    elif previous == None:
        # save scene ID values in a text file (one per line)
        displayID.to_csv(fileNameOne,
                         header=False, index=False, sep='\n')

    # generate text file as output
    with open(fileNameOne, 'r') as readFile:
        with open(fileNameTwo, 'w') as writeFile:
            writeFile.write(missionHeader + '\n')
            for line in readFile:
                writeFile.write(line)

    # remove temp txt file
    os.remove(fileNameOne)

    print("Use the following file as input in USGS API:\n", fileNameTwo, "\n")

######################################################################################
# Enter your own parameters here, save file, and run code. Pay attention to directory!

USGScsvFile = "LANDSAT_OT_C2_L2.csv"            # Example: "LANDSAT_OT_C2_L2.csv"
usgsPaths = [197, 198, 199]                     # Example: [197, 198, 199]
usgsRows = [30, 31, 32]                         # Example: [30, 31, 32]
usgsTier = "T1"                                 # Example: "T1" or "T2"
cloudCover = 15                                 # Example: 15
timeFrom = "2020-07-01"                         # Example: "2020-07-28"
timeTo = "2021-07-01"                           # Example: "2021-07-28"
previousScenes = "folder/oldScenes_file.txt"    # Example: "folder/oldScenes.txt" OR None
LandsatMission = "L8L2"
# Mission Options:
# Landsat 4-5 (Thematic Mapper) Level-1: "TML1"
# Landsat 4-5 (Thematic Mapper) Level-2: "TML2"
# Landsat 7 (Enhanced Thematic Mapper Plus) Level-1: "ETML1"
# Landsat 7 (Enhanced Thematic Mapper Plus) Level-2: "ETML2"
# Landsat 8 (OLI/TIRS) Level-1: "L8L1"
# Landsat 8 (OLI/TIRS) Level-2: "L8L2"


getUSGSCollTwoMetadata(USGScsvFile, usgsPaths,
                       usgsRows, usgsTier, cloudCover, timeFrom, timeTo, previousScenes, LandsatMission)

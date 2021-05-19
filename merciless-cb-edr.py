#!/usr/bin/env python
import sys
import cbapi.six as six
from cbapi.six import iteritems
from cbapi.response import Process  # Why not under models?
from cbapi.response.models import Alert, BannedHash, Binary, Feed, Sensor, SensorGroup, Site, Watchlist
from cbapi.example_helpers import build_cli_parser, get_cb_response_object  # needed?
from cbapi.errors import ApiError, ObjectNotFoundError, ServerError
import logging  # https://docs.python.org/3/howto/logging.html
from os import system, name  # for clearning the screen
from datetime import datetime, timedelta
# from cbapi.response import CbEnterpriseResponseAPI
import json
import csv
import random
from termcolor import colored, cprint  # https://pypi.org/project/termcolor/
# Menu packages - https://github.com/aegirhall/console-menu
#from consolemenu import *
#from consolemenu.items import *

import time
import sqlite3

log = logging.getLogger(__name__)


if six.PY3:
    confirm_input = input
else:
    confirm_input = raw_input  # noqa: F821


def main():

    parser = build_cli_parser()
    args = parser.parse_args()
    # Testing for exception primarily for cases where an api token and url aren't supplied
    try:
        cb = get_cb_response_object(args)
    except:
        print("Silly rabbit. Something went wrong. Did you forget your API Token and URL in the ./.carbonblack/credentials.response folder?")
        sys.exit()

    # print(cb.credentials)
    # watchlist_list(cb)
    # watchlist_export(cb)
    screen_clear()
    menu_main(cb)


def menu_main(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Main Menu***")
    print("1. Threat Intelligence Feeds")
    print("2. Alerts")
    print("3. Watchlists")
    print("4. Process Search")
    print("5. Binary Search")
    print("6. Sensors")
    print("7. Kitchen Sink")
    print("8. Inspire Me")
    print("9. Exit")
    selection = input("Enter choice: ")
    if selection == "1":
        screen_clear()
        menu_feeds(cb)
    elif selection == "2":
        screen_clear()
        menu_alerts(cb)
    elif selection == "3":
        screen_clear()
        menu_watchlists(cb)
    elif selection == "4":
        screen_clear()
        menu_processSearch(cb)
    elif selection == "5":
        screen_clear()
        menu_binarySearch(cb)
    elif selection == "6":
        screen_clear()
        menu_sensors(cb)
    elif selection == "7":
        screen_clear()
        menu_kitchenSink(cb)
    elif selection == "8":
        screen_clear()
        # print(quote_generator())
        cprint(quote_generator(), 'blue', 'on_white')
        print(" ")
        menu_main(cb)
    elif selection == "9":
        screen_clear()
        print("So long, farewell, auf Wiedersehen, adieu...")
        sys.exit()
    else:
        screen_clear()
        # print("ERROR: That was not a valid choice. Are you dunk?")
        cprint("ERROR: That was not a valid choice. Are you dunk?",
               'red', "on_white")
        print(" ")
        print(" ")
        menu_main(cb)


def menu_feeds(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Threat Intelligence Feed Menu***")
    print("1. Export Feed Summary")
    print("2. Export Feed By ID")
    print("3. Export All Feeds")
    print("4. Return To Main Menu")
    selection = input("Enter choice: ")
    if selection == "1":
        feed_exportSummary(cb)
    elif selection == "2":
        screen_clear()
        feed_exportById(cb)
    elif selection == "3":
        screen_clear()
        feed_exportAll(cb)
    elif selection == "4":
        screen_clear()
        menu_main(cb)
    else:
        screen_clear()
        # print("ERROR: That was not a valid choice. Are you high?")
        cprint("ERROR: That was not a valid choice. Are you high?",
               'red', "on_white")
        print(" ")
        print(" ")
        menu_watchlists(cb)


def menu_alerts(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Alerts Menu***")
    print("")
    input("This feature is under construction. Press ENTER to continue.")
    screen_clear()
    menu_main(cb)


def menu_watchlists(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Watchlist Menu***")
    print("1. Export Watchlist Summary")
    print("2. Export Watchlist By ID")
    print("3. Export All Watchlists")
    print("4. Return To Main Menu")
    selection = input("Enter choice: ")
    if selection == "1":
        watchlist_exportSummary(cb)
    elif selection == "2":
        screen_clear()
        watchlist_exportById(cb)
    elif selection == "3":
        screen_clear()
        watchlist_exportAll(cb)
    elif selection == "4":
        screen_clear()
        menu_main(cb)
    else:
        screen_clear()
        # print("ERROR: That was not a valid choice. Are you high?")
        cprint("ERROR: That was not a valid choice. Are you high?",
               'red', "on_white")
        print(" ")
        print(" ")
        menu_watchlists(cb)


def menu_processSearch(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Process Search***")
    print("")
    processQuery = input("Enter your query and press ENTER. Just press ENTER to return to the main menu.")
    if processQuery == "":
        screen_clear()
        menu_main(cb)
    else:
        queryType = "manualProcess"
        query = processQuery
        id = 0
        writeCsv_process(cb, id, queryType, query)           
 
           






    


def menu_binarySearch(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Binary Search***")
    print("")
    input("This feature is under construction. Press ENTER to continue.")
    screen_clear()
    menu_main(cb)


def menu_sensors(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Sensor Menu***")
    print("1. Export All Sensors")
    print("2. Return To Main Menu")
    selection = input("Enter choice: ")
    if selection == "1":
        sensors_exportSummary(cb)
    elif selection == "2":
        screen_clear()
        menu_main(cb)
    else:
        screen_clear()
        # print("ERROR: That was not a valid choice. Are you high?")
        cprint("ERROR: That was not a valid choice. Are you high?",
               'red', "on_white")
        print(" ")
        print(" ")
        menu_sensors(cb)


def menu_kitchenSink(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Kitchen Sink***")
    print("")
    input("This feature is under construction. Press ENTER to continue.")
    screen_clear()
    menu_main(cb)


def screen_clear():
    # check for system type so appropriate clear screen method is used
    if name == 'nt':
        _ = system('cls')
     # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def watchlist_exportSummary(cb):
    # Create csv file and prepare to write
    # encoding='utf-8' added courtesy of Ryan Boyle. Thanks!
    with open('watchlist_summary.csv', mode='w', newline='', encoding='utf-8') as outputFile:
        # If data from Carbon Black contains a comma, surround in quotes before sending to csv.
        myWatchlistWriter = csv.writer(
            outputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write header row
        myWatchlistWriter.writerow(['Name',
                                    'ID',
                                    'Index Type',
                                    'Alliance ID',
                                    'From Alliance',
                                    'Date Added',
                                    'Last Hit Date',
                                    'Last Hit Count',
                                    'Total Hits',
                                    'Count',
                                    'Search Query',
                                    'Query',
                                    'Enabled',
                                    'Description'])
        count = 0
        for myWatchlist in cb.select(Watchlist):
            # Assigning each watchlist value to a variable. Could be unnecessary, but makes it easier and cleaner if the value requires manipulation before writing to an output file.

            myName = myWatchlist.name
            myId = myWatchlist.id
            myIndexType = myWatchlist.index_type
            myFromAlliance = myWatchlist.from_alliance
            myAllianceId = myWatchlist.alliance_id
            myDateAdded = myWatchlist.date_added
            myLastHitDate = myWatchlist.last_hit
            myLastHitCount = myWatchlist.last_hit_count
            myTotalHits = myWatchlist.total_hits
            # count is resource intensive and depends on whether the watchlist is for processes or binaries. The other hit fields don't seem to accurately capture the # of items in the watchlist, so performing a separate query and counting.
            if myIndexType == "modules":
                myCount = cb.select(Binary).where(
                    myWatchlist.query)._count()
            elif myIndexType == "events":
                myCount = cb.select(Process).where(
                    myWatchlist.query)._count()
            else:
                # Should always be Modules/Binary or Events/Process but just in case...
                myCount = "?"
            # Shouldn't be neede be have had other areas where None is returned instead of zero so just in case.
            if myCount is None:
                myCount = 0
            mySearchQuery = myWatchlist.search_query
            myQuery = myWatchlist.query
            myEnabled = myWatchlist.enabled
            myDescription = myWatchlist.description

            # Write row to CSV
            myWatchlistWriter.writerow([myName,
                                        myId,
                                        myIndexType,
                                        myAllianceId,
                                        myFromAlliance,
                                        myDateAdded,
                                        myLastHitDate,
                                        myLastHitCount,
                                        myTotalHits,
                                        myCount,
                                        mySearchQuery,
                                        myQuery,
                                        myEnabled,
                                        myDescription])
            count += 1  # increment count - tracking total number of watchlists
    screen_clear()
    cprint('A watchlist summary, including ' + str(count) +
           ' watchlists was exported as "watchlist_summary.csv" Have a nice day.', 'green')
    print(" ")
    menu_watchlists(cb)


def watchlist_exportById(cb):
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Watchlist Export By ID Menu***")
    idList = []  # track all valid IDs
    myWatchlist_list = []
    # save all watchlist data into a list. Future processing against the list in memory.
    for myWatchlist in cb.select(Watchlist):
        myWatchlist_list.append(myWatchlist)
    # Column headers
    print("ID       INDEX TYPE   HITS         NAME")
    print("--       ----------   ----         ----")
    # Iterate through all watchlists
    for myWatchlist in myWatchlist_list:
        # Add IDs to a separate list.
        idList.append(myWatchlist.id)
        # Print ID, Type, Hits, Name
        # Weird issue with Hits. Watchlist properties total_hits and last_hit_count aren't accurate. One workaround is to querty the processes within and count, but this is resource intensive.
        myId = "{0:<9}".format(str(myWatchlist.id))
        # Have to account for binary watchlist vs process watchlist
        if myWatchlist.index_type == "modules":
            myIndexType = "{0:<13}".format("Binary")
            myWatchlistResults = cb.select(
                Binary).where(myWatchlist.query)
            myTotalHits = "{0:<13}".format(
                str(myWatchlistResults._count()))
        elif myWatchlist.index_type == "events":
            myIndexType = "{0:<13}".format("Process")
            myWatchlistResults = cb.select(
                Process).where(myWatchlist.query)
            myTotalHits = "{0:<13}".format(
                str(myWatchlistResults._count()))
        else:
            # Should always be Modules/Binary or Events/Process but just in case...
            myIndexType = "WTF?!"
            myWatchlistResults = "?"
        myName = myWatchlist.name
        # print the row data for current watchlist
        print(myId, end='')
        print(myIndexType, end='')
        print(myTotalHits, end='')
        print(myName)
    print("")
    idSelected = input(
        'Enter the ID of the Watchlist to export or enter nothing to go back: ')
    if idSelected not in idList:
        screen_clear()
        if idSelected == "":
            menu_watchlists(cb)
        else:
            cprint("ERROR: That was not a valid choice. Are you smoking crack again?",
                   'red', "on_white")
            print(" ")
            print(" ")
            watchlist_exportById(cb)
    else:
        # route based on whether a binary and process watchlist
        # if a different type is encountered, do nothing
        watchlist_whereClause = "id:" + str(idSelected)
        myWatchlist = cb.select(Watchlist).where(watchlist_whereClause).one()
        if myWatchlist.index_type == "events":
            writeCsv_process(cb, idSelected, "watchlist", "none")
        elif myWatchlist.index_type == "modules":
            writeCsv_binary(cb, idSelected, "watchlist", "none")
        print(" ")
        menu_watchlists(cb)


def watchlist_exportAll(cb):
    for myWatchlist in cb.select(Watchlist):
        if myWatchlist.index_type == "events":
            writeCsv_process(cb, myWatchlist.id, 'watchlist', "none")
        elif myWatchlist.index_type == "modules":
            writeCsv_binary(cb, myWatchlist.id, 'watchlist', "none")
    screen_clear()
    cprint('The Watchlist export is complete. Have a nice day.', 'green')
    menu_watchlists(cb)


def sensors_exportSummary(cb):
    # Create csv file and prepare to write
    # encoding='utf-8' added courtesy of Ryan Boyle. Thanks!
    with open('sensors_summary.csv', mode='w', newline='', encoding='utf-8') as outputFile:
        # If data from Carbon Black contains a comma, surround in quotes before sending to csv.
        mySensorWriter = csv.writer(
            outputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write header row
        mySensorWriter.writerow(['ID',
                                 'Build ID',
                                 'Build Version',
                                 'Up Time',
                                 'Sys Drive (bytes)',
                                 'Free Space (bytes)',
                                 'OS',
                                 'OS ID',
                                 'Memory (bytes)',
                                 'DNS Name',
                                 'NETBIOS Name',
                                 'Sensor Health Msg',
                                 'Computer SID',
                                 'Event Log Flush Time',
                                 'Check-in Time',
                                 'Network Adapters',
                                 'Sensor Health #',
                                 'Registration Time',
                                 'Next Check-in Time',
                                 'Boot Count',
                                 'Sensor Group',
                                 'Display',
                                 'Uninstall',
                                 'Parity Host ID',
                                 'Isolation Request',
                                 'Isolation Status'])
        count = 0
        #countTotal = cb.select(Sensor)._count()
        countTotal = 9999
        for mySensor in cb.select(Sensor):
            # Assigning each sensor value to a variable. Could be unnecessary, but makes it easier and cleaner if the value requires manipulation before writing to an output file.

            myId = mySensor.id
            myBuildId = mySensor.build_id
            myBuildVersionString = mySensor.build_version_string
            myUptime = mySensor.uptime
            mySystemvolumeTotalSize = mySensor.systemvolume_total_size
            mySystemvolumeFreeSize = mySensor.systemvolume_free_size
            myOsEnvironmentDisplayString = mySensor.os_environment_display_string
            myOsEnvironmentId = mySensor.os_environment_id
            myPhysicalMemorySize = mySensor.physical_memory_size
            myComputerDnsName = mySensor.computer_dns_name
            myComputerName = mySensor.computer_name
            mySensorHealthMsg = mySensor.sensor_health_message
            myComputerSid = mySensor.computer_sid
            myEventLogFlushTime = mySensor.event_log_flush_time
            myLastCheckinTime = mySensor.last_checkin_time
            myNetworkAdapters = mySensor.network_adapters
            mySensorHealthStatus = mySensor.sensor_health_status
            myRegistrationTime = mySensor.registration_time
            myNextCheckinTime = mySensor.next_checkin_time
            myBootId = mySensor.boot_id
            myGroupId = mySensor.group_id
            myDisplay = mySensor.display
            myUninstall = mySensor.uninstall
            myParityHostId = mySensor.parity_host_id
            myNetworkIsolationEnabled = mySensor.network_isolation_enabled
            myIsIsolating = mySensor.is_isolating

            # Write row to CSV
            mySensorWriter.writerow([myId,
                                     myBuildId,
                                     myBuildVersionString,
                                     myUptime,
                                     mySystemvolumeTotalSize,
                                     mySystemvolumeFreeSize,
                                     myOsEnvironmentDisplayString,
                                     myOsEnvironmentId,
                                     myPhysicalMemorySize,
                                     myComputerDnsName,
                                     myComputerName,
                                     mySensorHealthMsg,
                                     myComputerSid,
                                     myEventLogFlushTime,
                                     myLastCheckinTime,
                                     myNetworkAdapters,
                                     mySensorHealthStatus,
                                     myRegistrationTime,
                                     myNextCheckinTime,
                                     myBootId,
                                     myGroupId,
                                     myDisplay,
                                     myUninstall,
                                     myParityHostId,
                                     myNetworkIsolationEnabled,
                                     myIsIsolating])
            count += 1  # increment count - tracking total number of sensors
            if count % 100 == 0:
                screen_clear()
                cprint('Exporting: sensory_summary.csv Progress: ' + str(count) + ' of ' + str(
                    countTotal) + '(' + str(int(count/countTotal*100)) + ' %) - completed.', 'blue')
                print(" ")
    screen_clear()
    cprint('A sensor summary, including ' + str(count) +
           ' sensors was exported as "sensor_summary.csv" Have a nice day.', 'green')
    print(" ")
    menu_sensors(cb)


def feed_exportSummary(cb):    # Create csv file and prepare to write
    # encoding='utf-8' added courtesy of Ryan Boyle. Thanks!
    with open('feed_summary.csv', mode='w', newline='', encoding='utf-8') as outputFile:
        # If data from Carbon Black contains a comma, surround in quotes before sending to csv.
        myFeedWriter = csv.writer(
            outputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write header row
        myFeedWriter.writerow(['ID',
                               'Display Name',
                               'Internal Name',
                               'Process Count',
                               'Binary Count',
                               'Enabled',
                               'Summary',
                               'Tech Summary',
                               'Verify Server Cert',
                               'Manually Added',
                               'Display Order',
                               'Use Proxy',
                               'Provider URL',
                               'Feed URL'])

        count = 0
        for myFeed in cb.select(Feed):
            # Assigning each watchlist value to a variable. Could be unnecessary, but makes it easier and cleaner if the value requires manipulation before writing to an output file.
            myId = myFeed.id
            myDisplayName = myFeed.display_name
            myInternalName = myFeed.name

            # Received error messages where some counts returned None instead of 0
            if (myFeed.search_processes() is None):
                myProcessCount = "DISABLED"
            else:
                myProcessCount = myFeed.search_processes()._count()
            if (myFeed.search_binaries() is None):
                myBinaryCount = "DISABLED"
            else:
                myBinaryCount = myFeed.search_binaries()._count()

            myEnabled = myFeed.enabled
            mySummary = myFeed.summary
            myTechSummary = myFeed.tech_data
            myVerifyServerCert = myFeed.validate_server_cert
            myManuallyAdded = myFeed.manually_added
            myDisplayOrder = myFeed.order
            myUseProxy = myFeed.use_proxy
            myProviderUrl = myFeed.provider_url
            myFeedUrl = myFeed.feed_url

            # Write row to CSV
            myFeedWriter.writerow([myId,
                                   myDisplayName,
                                   myInternalName,
                                   myProcessCount,
                                   myBinaryCount,
                                   myEnabled,
                                   mySummary,
                                   myTechSummary,
                                   myVerifyServerCert,
                                   myManuallyAdded,
                                   myDisplayOrder,
                                   myUseProxy,
                                   myProviderUrl,
                                   myFeedUrl])
            count += 1  # increment count - tracking total number of feeds
    screen_clear()
    cprint('A feed summary, including ' + str(count) +
           ' feeds was exported as "feed_summary.csv" Have a nice day.', 'green')
    print(" ")
    menu_feeds(cb)


def feed_exportById(cb):
    myFeed_list = []
    idList = []
    print("<===Merciless Carbon Black Response/EDR Export Tool===>")
    print("")
    print("***Threat Intelligence Feed Export By ID Menu***")
    # Save all feeds into a list. Future processing against the list in memory
    for myFeed in cb.select(Feed):
        myFeed_list.append(myFeed)
    # Column headers
    print("ID   PROCESSES  BINARIES  NAME")
    print("--   ---------  --------  ----")
    # Iterate through all watchlists
    for myFeed in myFeed_list:
        # Add IDs to a separate list.
        # Had an issue with feed that wasn't present for watchlists. Watchlist IDs were automatically considered strings where feed IDs were more like Integers. When a user selects a feed ID, that value is a string. So, now converting to string explicitly below so will match type with user input later.

        idList.append(str(myFeed.id))

        # Print ID, Type, Hits, Name
        # Weird issue with Hits. Watchlist properties total_hits and last_hit_count aren't accurate. One workaround is to querty the processes within and count, but this is resource intensive.
        myId = "{0:<5}".format(str(myFeed.id))
        #myWhereClause = "id:" + str(myFeed.id)
        # Received error messages where some counts returned None instead of 0
        if (myFeed.search_processes() is None):
            myProcessCount = "{0:<11}".format("X")
        else:
            myProcessCount = "{0:<11}".format(
                str(myFeed.search_processes()._count()))
        if (myFeed.search_binaries() is None):
            myBinaryCount = "{0:<10}".format("X")
        else:
            myBinaryCount = "{0:<10}".format(
                str(myFeed.search_binaries()._count()))

        myDisplayName = myFeed.display_name
        myInternalName = myFeed.name
        # print the row data for current watchlist
        print(myId, end='')
        print(myProcessCount, end='')
        print(myBinaryCount, end='')
        print(myDisplayName + " (" + myInternalName + ")")
    print("")
    idSelected = input(
        'Enter the ID of the Feed to export or enter nothing to go back: ')
    if idSelected not in idList:
        screen_clear()
        if idSelected == "":
            menu_feeds(cb)
        else:
            cprint("ERROR: That was not a valid choice. Are you smoking meth again?",
                   'red', "on_white")
            print(" ")
            print(" ")
            feed_exportById(cb)
    else:
        # Feed will have processes and binaries exported unless feed is disabled.

        myWhereClause = "id:" + str(idSelected)
        myFeed = cb.select(Feed).where(myWhereClause).one()
        if myFeed.enabled == False:
            screen_clear()
            cprint("ERROR: That was not a valid choice. Disabled feeds cannot be exported. So silly.",
                   'red', "on_white")
            print(" ")
            print(" ")
            feed_exportById(cb)
        else:
            # continue to export feed
            writeCsv_process(cb, idSelected, "feed", "none")
            writeCsv_binary(cb, idSelected, "feed", "none")


def feed_exportAll(cb):
    # cb.dashboard_statistics
    pass


def writeCsv_process(cb, id, queryType, query):
    if queryType == "watchlist":
        watchlist_whereClause = "id:" + str(id)
        myWatchlist = cb.select(Watchlist).where(watchlist_whereClause).one()
        myResults = cb.select(Process).where(myWatchlist.query)
        myResultsCount = myResults._count()
        myFilename = myWatchlist.name
        myFilename_sanitized = 'watchlist-id-' + str(myWatchlist.id) + '_' + myFilename.translate(
            {ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~_=+"}) + '_processes'
    elif queryType == "feed":
        feed_whereClause = "id:" + str(id)
        # myWatchlist = cb.select(Watchlist).where(watchlist_whereClause).one()
        myFeed = cb.select(Feed).where(feed_whereClause).one()
        myResults = myFeed.search_binaries()
        myResultsCount = myResults._count()
        myFilename = myFeed.display_name + '_' + myFeed.name

        myFilename_sanitized = 'feed-id-' + str(id) + '_' + myFilename.translate(
            {ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~_=+"}) + '_processes'
    elif queryType == "manualProcess":
        myResults = cb.select(Process).where(query)
        myResultsCount = myResults._count()
        myFilename = "processQueryExportTest"
        myFilename_sanitized = "processQueryExportTest"
    else:
        sys.exit()
    # encoding='utf-8' added courtesy of Ryan Boyle. Thanks!
    with open(myFilename_sanitized + '.csv', mode='w', newline='', encoding='utf-8') as outputFile:
        # If data from Carbon Black contains a comma, surround in quotes before sending to csv.
        # encoding='utf-8' added courtesy of Ryan Boyle. Thanks!
        myResultsWriter = csv.writer(
            outputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        myResultsWriter.writerow(['Process CB ID',
                                  'Segment CB ID',
                                  'Process Name',
                                  'PID',
                                  'Process MD5',
                                  'Process Path',
                                  'Process Cmd Line',
                                  'Parent ID',
                                  'Parent Name',
                                  'Parent PID',
                                  'Last Update',
                                  'Start Time',
                                  'Hostname',
                                  'Username',
                                  'OS Type',
                                  'Host Type',
                                  'Modload',
                                  'Regmod',
                                  'Filemod',
                                  'Netconn',
                                  'ChildProc',
                                  'CrossProc',
                                  'Comms IP',
                                  'Interface IP',
                                  'Sensor ID',
                                  'Sensor Group'])
        count = 0
        for proc in myResults:
            # outputFile.write('%s' % proc.process_name, '%s' % proc.start, '%s' % proc.end, '%s' % proc.interface_ip,
            #              '%s' % proc.username, '%s' % proc.cmdline, '%s' % proc.parent_md5, '%s' % proc.webui_link)
            myProcessId = proc.id
            # myProcessId = proc.process_id (Couldn't get results from this field)
            mySegmentId = proc.segment_id
            myProcessName = proc.process_name
            myProcessPid = proc.process_pid
            myProcessMd5 = proc.process_md5
            myPath = proc.path
            myCmdline = proc.cmdline
            myParentId = proc.parent_id
            myParentName = proc.parent_name
            # parent_md5 throws error sometimes. Null check doesn't work
            # myParentMd5 = proc.parent_md5
            myParentPid = proc.parent_pid
            myLastUpdate = proc.last_update
            myStartTime = proc.start
            myHostname = proc.hostname
            myUsername = proc.username
            myOsType = proc.os_type
            myHostType = proc.host_type
            # myRegmodComplete = proc.regmod_complete
            # myFilemodComplete = proc.filemod_complete
            # myModloadComplete = proc.modload_complete
            # myNetconnComplete = proc.netconn_complete
            # myChildprocComplete = proc.childproc_complete
            # myCrossprocComplete = proc.crossproc_complete
            myModuleCount = proc.modload_count
            myRegModCount = proc.regmod_count
            myFileModCount = proc.filemod_count
            myNetConn = proc.netconn_count
            myChildProc = proc.childproc_count
            myCrossProc = proc.crossproc_count
            myCommsIp = proc.comms_ip
            myInterfaceIp = proc.interface_ip
            mySensorId = proc.sensor_id
            mySensorGroupId = proc.group

            myResultsWriter.writerow([myProcessId,
                                      mySegmentId,
                                      myProcessName,
                                      myProcessPid,
                                      myProcessMd5,
                                      myPath,
                                      myCmdline,
                                      myParentId,
                                      myParentName,
                                      myParentPid,
                                      myLastUpdate,
                                      myStartTime,
                                      myHostname,
                                      myUsername,
                                      myOsType,
                                      myHostType,
                                      myModuleCount,
                                      myRegModCount,
                                      myFileModCount,
                                      myNetConn,
                                      myChildProc,
                                      myCrossProc,
                                      myCommsIp,
                                      myInterfaceIp,
                                      mySensorId,
                                      mySensorGroupId
                                      ])
            count += 1
            if count % 1000 == 0:
                screen_clear()
                cprint('Exporting: "' + myFilename_sanitized + '.csv"' + ' Progress: ' +
                       str(count) + ' of ' + str(myResultsCount) + '(' + str(int(count/myResultsCount*100)) + '%) - completed.', 'blue')
                print(" ")
    screen_clear()
    cprint('The ' + queryType + ' was exported as "' +
           myFilename_sanitized + '.csv". Have a nice day.', 'green')
    time.sleep(1)  # slight pause in case msg changes too quickly


def writeCsv_binary(cb, id, queryType, query):
    if queryType == "watchlist":
        watchlist_whereClause = "id:" + str(id)
        myWatchlist = cb.select(Watchlist).where(watchlist_whereClause).one()
        myResults = cb.select(Binary).where(myWatchlist.query)
        myResultsCount = myResults._count()
        myFilename = myWatchlist.name
        myFilename_sanitized = 'watchlist-id-' + str(myWatchlist.id) + '_' + myFilename.translate(
            {ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~_=+"}) + "_binaries"
    elif queryType == "feed":
        feed_whereClause = "id:" + str(id)
        # myWatchlist = cb.select(Watchlist).where(watchlist_whereClause).one()
        myFeed = cb.select(Feed).where(feed_whereClause).one()
        myResults = myFeed.search_processes()
        myResultsCount = myResults._count()
        myFilename = myFeed.display_name + '_' + myFeed.name

        myFilename_sanitized = 'feed-id-' + str(id) + '_' + myFilename.translate(
            {ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~_=+"}) + "_binaries"
    else:
        sys.exit()
    # encoding='utf-8' added courtesy of Ryan Boyle. Thanks!
    with open(myFilename_sanitized + '.csv', mode='w', newline='', encoding='utf-8') as outputFile:
        # If data from Carbon Black contains a comma, surround in quotes before sending to csv.
        myResultsWriter = csv.writer(
            outputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        myResultsWriter.writerow(['Binary MD5',
                                  'First Received',
                                  'Filesize(bytes)',
                                  'SizeCopied(bytes)'])
        count = 0
        for myBinary in myResults:
            myMd5 = myBinary.md5
            myServerAddedTimestamp = myBinary.server_added_timestamp
            myOrigModLen = myBinary.orig_mod_len
            myCopiedModLen = myBinary.copied_mod_len

            myResultsWriter.writerow([myMd5,
                                      myServerAddedTimestamp,
                                      myOrigModLen,
                                      myCopiedModLen])
            count += 1
            if count % 1000 == 0:
                screen_clear()
                cprint('Exporting: "' + myFilename_sanitized + '.csv"' + ' Progress: ' +
                       str(count) + ' of ' + str(myResultsCount) + '(' + str(int(count/myResultsCount*100)) + '%) - completed.', 'blue')
                print(" ")
    screen_clear()
    cprint('The ' + queryType + ' was exported as "' +
           myFilename + '.csv". Have a nice day.', 'green')
    time.sleep(1)  # slight pause in case msg changes too quickly


def quote_generator():
    quotes = ["If at first you don't succeed, then skydiving is definitely not for you. ~Steven Wright",
              "All you need in this life is ignorance and confidence, and then success is sure. ~Mark Twain",
              "Age is of no importance unless you're a cheese. ~Billie Burke",
              "Friendship is like peeing on yourself: everyone can see it, but only you get the warm feeling that it brings. ~Robert Bloch",
              "The difference between genius and stupidity is; genius has its limits. ~Albert Einstein",
              "Never put off until tomorrow what you can do the day after tomorrow. ~Mark Twain",
              "The more you weigh, the harder you are to kidnap. Stay safe. Eat cake. ~Unknown",
              "Be who you are and say what you feel, because those who mind don't matter and those who matter don't mind. ~Bernard Baruch",
              "Money won't buy happiness, but it will pay the salaries of a large research staff to study the problem. ~Bill Vaughan",
              "We never really grow up, we only learn how to act in public. ~Bryan White",
              "42. ~Deep Thought"]
    return random.choice(quotes)


if __name__ == "__main__":
    sys.exit(main())

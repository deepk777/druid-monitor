#vim: set fileencoding=utf-8

import argparse
import sys
from druid_base import *

def parse_args():
    parser = argparse.ArgumentParser(description='druid monitor utility ')
    parser.add_argument('-c','--cfile', action="store", 
            dest="cfile", default="druid.conf",
            help=convert_sys_encode('IP地址配置文件,默认值为druid.conf')
            )

    parser.add_argument('-n','--id', action="store", 
            dest="sql_id", 
            help=convert_sys_encode('要打印详细信息的sql的id'))

    parser.add_argument('--host', action="store", 
            dest="host", 
            help=convert_sys_encode('主机名, 要跟cfile里的配置一致,根据主机名查找url')
            )
    return parser.parse_args()

def print_sql_detailInfo(url, sql_id , color_info):
    rows = []
    result = fetch_json_result(url,"/druid/sql-" + str(sql_id) + ".json")
    data_content = result.get("Content")

    formattedSql = data_content.get("formattedSql")
    if formattedSql == None :
        formattedSql = data_content.get("SQL")
    print "SQL:"
    print "=" * 80
    print formattedSql 
    print "=" * 80
    print "" 

    print "Slow Sql:"
    print "=" * 80
    print "MaxTimespan:", get_colored_value(color_info, data_content.get("MaxTimespan"),"MaxTimespan")
    print "MaxTimespanOccurTime:", convert_time(data_content.get("MaxTimespanOccurTime"))
    print "LastSlowParameters:",data_content.get("LastSlowParameters")
    print "=" * 80
    print "" 

    print "DbType:",data_content.get("DbType")
    print "ExecuteCount:" , get_colored_value(color_info, data_content.get("ExecuteCount"),"ExecuteCount")
    print "LastTime:", data_content.get("LastTime")
    histogram = get_colored_histo(color_info, data_content.get("Histogram"),"Histogram")
    print "Histogram:",histogram
    holdHistor = get_colored_histo(color_info , data_content.get("ExecuteAndResultHoldTimeHistogram"),"ExecuteAndResultHoldTimeHistogram")
    print "ExecuteAndHoldHistor:",holdHistor
    fetchRowHistor = get_colored_histo(color_info, data_content.get("FetchRowCountHistogram"),"FetchRowCountHistogram")
    print "FetchRowHisto:", fetchRowHistor
    print "ErrorCount:", data_content.get("ErrorCount")
    print "EffectedRowCountHistogram:" , data_content.get("EffectedRowCountHistogram")
    print "ConcurrentMax:", data_content.get("ConcurrentMax")
    print "TotalTime:", data_content.get("TotalTime")
    print "BatchSizeMax:", data_content.get("BatchSizeMax")
    print "RunningCount:",data_content.get("RunningCount")
    print "FetchRowCountTotal:", data_content.get("FetchRowCount")
    print "FetchRowCountMax:", data_content.get("FetchRowCountMax")
    print "EffectedRowCountTotal:",data_content.get("EffectedRowCount")
    print "EffectedRowCountMax:",data_content.get("EffectedRowCountMax")

    #row.append(data_content.get("ResultSetHoldTime"))
    #row.append(data_content.get("InTransactionCount"))
    #row.append(data_content.get("ID"))

if __name__ == "__main__" :
    args_info = parse_args()
    host_info = read_conf(args_info.cfile)
    color_info = read_color_conf()

    if args_info.host == None :
        print "please specify host with --host argument"
        sys.exit()

    if args_info.sql_id == None :
        print "please specify sql_id with --id argument"
        sys.exit()

    url = host_info[args_info.host]
    print_sql_detailInfo(url , args_info.sql_id, color_info)
    


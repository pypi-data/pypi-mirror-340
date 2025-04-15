import os
import asyncio
import jpype
from pydtc.connection import DBClient, APIClient
from pydtc.parallelize import ParallelDataFrame

def connect(db, host, user, password, jvm_args=None, props=None, charset='latin-1s', classname=None, lib_path=None, runtime_path=None):
    '''
    Interface to connect to the database

    Param:
      db: the common name of the database, e.g db2, teradata
      host: the host of the database instance
      user: user name, principal if connect to hive thru kerberos auth
      passowrd: user password, keytab location if connect to hive thru kerberos auth
      props: the java property that to be set system-wide
      classname: the classname, e.g. "com.mysql.jdbc.Driver"
      lib_path: the jdbc driver location
      runtime_path: the java runtime path if custom desired
    '''
    con = DBClient(db, host, user, password, jvm_props=jvm_args, java_props=props, charset=charset, classname=classname, lib_path=lib_path, runtime_path=runtime_path)
    con.connect()

    return con

def connect_dbapi(db, host, user, password, props={}, charset='latin-1', classname=None, lib_path=None, runtime_path=None):
    '''
    Return jaydebeapi Connection object that complies to DBAPI 2.0

    Param:
      db: the common name of the database, e.g db2, teradata
      host: the host of the database instance
      user: user name, principal if connect to hive thru kerberos auth
      passowrd: user password, keytab location if connect to hive thru kerberos auth
      props: the java property that to be set system-wide
      classname: the classname, e.g. "com.mysql.jdbc.Driver"
      lib_path: the jdbc driver location
      runtime_path: the java runtime path if custom desired
    '''
    con = DBClient(db, host, user, password, java_props=props, charset=charset, classname=classname, lib_path=lib_path, runtime_path=runtime_path)
    con.connect()

    return con._conn

def read_sql(sql, con):

    return con.read_sql(sql)

def clob_to_str(clob):
    try:
        return clob.getSubString(1, int(clob.length()))
    except Exception as err:
        return str(err)[:200]

def blob_to_file(blob, file_name, save_to):
    '''
    helper func to save the blob field into file.
    Param:
      blob: the blob field
      file_name: the file name
      save_to: the folder to save the file
    '''
    try:
        out = jpype.java.io.FileOutputStream(os.path.join(save_to, file_name))
        buff = blob.getBytes(1, int(blob.length()))
        out.write(buff)
        out.close()
        return 'Success'
    except Exception as err:
        return str(err)[:200]

def create_temp(sql, con):

    con.create_temp(sql)

def load_temp(sql, con, df, chunksize=10000):

    con.load_temp(sql, df, chunksize=chunksize)

def load_batch(sql, con, df, chunksize=10000):

    con.load_batch(sql, df, chunksize=chunksize)


# speed up pandas cpu operation with multiprocessing especially for large set.
def p_apply(func, df, chunksize=10000, cores=None):
    try:
        pdf = ParallelDataFrame(df, num_ps=cores)

        return pdf.apply(func, chunksize=chunksize)
    except:
        raise
    finally:
        pdf.close()


def p_groupby_apply(func, df, groupkey, cores=None):
    try:
        pdf = ParallelDataFrame(df, num_ps=cores)

        return pdf.group_apply(func, groupkey)
    except:
        raise
    finally:
        pdf.close()


def api_get(urls, auth=None, loop=None):
    try:
        loop = loop or asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        api = APIClient(auth=auth, loop=loop)

        if isinstance(urls, list):
            _results = loop.run_until_complete(api.fetch_all(urls))

            results = [{url : r} for url, r in zip(urls, _results)]

        else:
            _results = loop.run_until_complete(api.fetch(urls))

            results = {urls : _results}

        return results
    except:
        raise
    finally:
        asyncio.run(api.close())


def api_update(url, data=None, method='put', auth=None, loop=None):
    try:
        loop = loop or asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        api = APIClient(auth=auth, loop=loop)

        results = loop.run_until_complete(api.update(url, data=data, method=method))

        return results
    except:
        raise
    finally:
        asyncio.run(api.close())
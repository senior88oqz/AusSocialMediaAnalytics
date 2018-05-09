import json
import os
import time
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from queue import Queue
from threading import Thread

import click
import couchdb
import psutil
import tweepy
from couchdb.http import ResourceNotFound

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
STOP_FLAG = '__STOP_FLAG__'


class Key(object):
    def __init__(self, filename):
        jobj = json.load(open(filename, 'r'))
        self.name = jobj['name']
        self.consumer_key = jobj['consumer_key']
        self.consumer_secret = jobj['consumer_secret']
        self.access_token = jobj['access_token']
        self.access_secret = jobj['access_secret']
        self.stream_name = jobj['stream_name']
        self.stream_grid = jobj['stream_grid']
        self.search_name = jobj['search_name']
        self.search_geocode = jobj['search_geocode']


class WorkerStatus(object):
    def __init__(self, key):
        self.key = key
        self.count = 0
        self.valid = 0
        self.update = datetime.now()
        self.error = None


def getkeys(dirname):
    keys = []
    for filename in os.listdir(dirname):
        try:
            key = Key(os.path.join(dirname, filename))
            keys.append(key)
        except Exception:
            pass
    return keys


def getapi(key):
    auth = tweepy.OAuthHandler(key.consumer_key, key.consumer_secret)
    auth.set_access_token(key.access_token, key.access_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)


def format_size(num):
    if not isinstance(num, int):
        num = int(num)
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%4.2f%s%s" % (num, unit, 'B')
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Y', 'B')


def preprocess(tweet):
    t = tweet

    u = t['user']
    t['_id'] = t['id_str']

    u.pop('profile_background_color', None)
    u.pop('profile_background_image_url', None)
    u.pop('profile_background_image_url_https', None)
    u.pop('profile_background_tile', None)
    u.pop('profile_image_url', None)
    u.pop('profile_image_url_https', None)
    u.pop('profile_banner_url', None)
    u.pop('profile_link_color', None)
    u.pop('profile_sidebar_border_color', None)
    u.pop('profile_sidebar_fill_color', None)
    u.pop('profile_text_color', None)
    u.pop('profile_use_background_image', None)
    u.pop('default_profile', None)
    u.pop('default_profile_image', None)

    if 'retweeted_status' in t:
        ru = t['retweeted_status']['user']
        ru.pop('profile_background_color', None)
        ru.pop('profile_background_image_url', None)
        ru.pop('profile_background_image_url_https', None)
        ru.pop('profile_background_tile', None)
        ru.pop('profile_image_url', None)
        ru.pop('profile_image_url_https', None)
        ru.pop('profile_banner_url', None)
        ru.pop('profile_link_color', None)
        ru.pop('profile_sidebar_border_color', None)
        ru.pop('profile_sidebar_fill_color', None)
        ru.pop('profile_text_color', None)
        ru.pop('profile_use_background_image', None)
        ru.pop('default_profile', None)
        ru.pop('default_profile_image', None)


def is_valid(tweet):
    return tweet['coordinates'] is not None


def get_couchdb(url, tablename='tweets'):
    couch = couchdb.Server(url)
    try:
        db = couch[tablename]
    except ResourceNotFound:
        db = couch.create(tablename)
    except ConnectionRefusedError:
        return None
    return db


def wait_for_exit():
    while True:
        try:
            c = click.getchar()
            if c in ['q', 'Q', '\x03', b'q', b'Q', b'\x03']:
                return
        except KeyboardInterrupt:
            return


class StreamListener(tweepy.StreamListener):
    def __init__(self, status, queue, no_filter):
        self.status = status
        self.queue = queue
        self.no_filter = no_filter

    def on_data(self, raw_data):
        self.status.count += 1
        self.status.update = datetime.now()
        self.status.error = None
        tweet = json.loads(raw_data)
        if self.no_filter or is_valid(tweet):
            self.status.valid += 1
            self.queue.put(tweet)

    def on_error(self, status_code):
        self.status.error = str(status_code)


def worker_stream(key, status, queue, no_filter):
    api = getapi(key)
    while True:
        try:
            stream = tweepy.Stream(auth=api.auth, listener=StreamListener(status, queue, no_filter))
            stream.filter(locations=key.stream_grid)
        except tweepy.TweepError as e:
            status.error = str(e)
            time.sleep(15 * 60)
            api = getapi(key)


def worker_search(key, status, queue, no_filter):
    api = getapi(key)
    max_id = None
    while True:
        try:
            if max_id is not None:
                tweets = api.search(q='', geocode=key.search_geocode, max_id=max_id)
            else:
                tweets = api.search(q='', geocode=key.search_geocode)

            if len(tweets) > 0:
                max_id = min(tweets.ids())
            else:
                max_id = None
                continue

            for tweet in tweets:
                status.count += 1
                status.update = datetime.now()
                status.error = None
                tweet = tweet._json
                if no_filter or is_valid(tweet):
                    status.valid += 1
                    queue.put(deepcopy(tweet))

        except tweepy.TweepError as e:
            status.error = str(e)
            time.sleep(15 * 60)


def worker_write(out_path, db, queue, cache_size):
    cache = []
    if out_path is not None:
        out_fp = open(out_path, 'a', encoding='utf-8')
    else:
        out_fp = None
    while True:
        tweet = queue.get()
        if tweet == STOP_FLAG:
            break

        preprocess(tweet)
        if db is not None:
            cache.append(tweet)
            if len(cache) > cache_size:
                db.update(cache)
                cache.clear()
        if out_fp is not None:
            out_fp.write(json.dumps(tweet) + '\n')
            out_fp.flush()

    # Clean up
    if db is not None and cache:
        db.update(cache)
    if out_fp is not None:
        out_fp.flush()
        out_fp.close()


def worker_log(log_path, stream_status, search_status, queue, db, out_path, stop_flag, use_filter, silence):
    start_time = datetime.now()
    psinfo = psutil.Process()

    def log_flush(cache):
        content = ''.join(cache)
        click.clear()
        if not silence:
            print(content.replace('\n', '\r\n'), end='')
        if log_path is not None:
            with open(log_path, 'w') as log_fp:
                log_fp.write(content.replace('\n', os.linesep))
                log_fp.flush()

    while True:
        if not stop_flag[0]:
            log_cache = []

            def log(content='', end='\n'):
                log_cache.append(content + end)

            # Prepare results
            now = datetime.now()
            seconds = (now - start_time).total_seconds()

            stream_count = 0
            search_count = 0
            all_valid = 0
            for s in stream_status:
                stream_count += s.count
                all_valid += s.valid
            for s in search_status:
                search_count += s.count
                all_valid += s.valid
            all_count = stream_count + search_count

            tweetps = all_count / seconds if seconds > 0 else 0
            validps = all_valid / seconds if seconds > 0 else 0
            queue_size_str = ' (%d)' % queue.qsize() if not queue.empty() else ''

            # General log
            log('Started at %s' % str(start_time)[:-7])
            log('Last log time: %s\t(%s)' % (str(now)[:-7], str(now - start_time)[:-7]))
            if use_filter:
                log('Threads: %d\tMemory: %s\tTweet Count: %6d / %-7d%s' % (
                    psinfo.num_threads(), format_size(psinfo.memory_info().rss), all_valid, all_count, queue_size_str))
                log('Harvest rate: %.2f valid tweet/static (%.2f tweet/static)' % (validps, tweetps))
            else:
                log('Threads: %d\tMemory: %s\tTweet Count: %d%s' % (
                    psinfo.num_threads(), format_size(psinfo.memory_info().rss), all_count, queue_size_str))
                log('Harvest rate: %.2f tweet/static' % tweetps)

            # CouchDB log
            if db is not None:
                dbinfo = db.info()
                log('CouchDB connected')
                log('CouchDB documents: %d' % dbinfo['doc_count'])
                log('CouchDB results size: %s' % format_size(dbinfo['data_size']))
            else:
                log('CouchDB disconnected')

            # Raw file log
            if out_path is not None:
                out_filesize = os.path.getsize(out_path) if os.path.isfile(out_path) else 0
                log('Output file: %s\t(%s)' % (out_path, format_size(out_filesize)))
            else:
                log('Output file disabled')
            log('-' * 20)
            # Stream log
            log('Stream count: %d' % stream_count)
            for status in stream_status:
                td = now - status.update
                if use_filter:
                    log('[%s]: %6d / %-7d' % (status.key.stream_name, status.valid, status.count), end='')
                else:
                    log('[%s]: %-7d' % (status.key.stream_name, status.count), end='')
                if td > timedelta(minutes=1):
                    log(' Idle: [%s]' % str(td)[:-7], end='')
                if status.error:
                    log(' Error: [%s]' % status.error, end='')
                log()
            log('-' * 20)
            # Search log
            log('Search count: %d' % search_count)
            for status in search_status:
                td = now - status.update
                if use_filter:
                    log('[%s]: %6d / %-7d' % (status.key.search_name, status.valid, status.count), end='')
                else:
                    log('[%s]: %-7d' % (status.key.search_name, status.count), end='')
                if td > timedelta(minutes=1):
                    log(' Idle: [%s]' % str(td)[:-7], end='')
                if status.error:
                    log(' Error: [%s]' % status.error, end='')
                log()

            log_flush(log_cache)
            time.sleep(1)


help_texts = {
    '-i': 'Local file input (not API)   None',
    '-k': 'Twitter API keys dir path    keys',
    '-a': 'Use all tweets (no filter)   False',
    '-l': 'Log file path                None',
    '-o': 'Output file path             None',
    '-n': 'Disable CouchDB              False',
    '-t': 'CouchDB table name           tweets',
    '-u': 'CouchDB url                  localhost:5984',
    '-c': 'CouchDB update cache size    200',
    '-s': 'Do not use stdout output     False',
}
keys_type = click.Path(exists=True, file_okay=False, resolve_path=True)
log_type = click.Path(writable=True, dir_okay=False, resolve_path=True)
input_type = click.Path(exists=True, resolve_path=True)
output_type = click.Path(writable=True, dir_okay=False, resolve_path=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--input', '-i', 'in_path', default=None, type=input_type, help=help_texts['-i'])
@click.option('--keys-path', '-k', type=keys_type, default='keys', help=help_texts['-k'])
@click.option('--all', '-a', 'no_filter', is_flag=True, default=False, help=help_texts['-a'])
@click.option('--log', '-l', 'log_path', default=None, type=log_type, help=help_texts['-l'])
@click.option('--output', '-o', 'out_path', default=None, type=output_type, help=help_texts['-o'])
@click.option('--no-couchdb', '-n', is_flag=True, help=help_texts['-n'])
@click.option('--table-name', '-t', default='tweets', help=help_texts['-t'])
@click.option('--database-url', '-u', default='http://localhost:5984', metavar='URL', help=help_texts['-u'])
@click.option('--cache-size', '-c', default=200, type=click.INT, help=help_texts['-c'])
@click.option('--silence', '-s', is_flag=True, help=help_texts['-s'])
def main(in_path, no_filter, keys_path, no_couchdb, database_url, table_name, cache_size, out_path, log_path, silence):
    # Get the CouchDB connection
    if no_couchdb:
        db = None
    else:
        db = get_couchdb(database_url, table_name)

    if no_couchdb and not out_path:
        print('There is no output! (Both CouchDB and file output are disabled!)')
        return

    # Writer thread
    queue = Queue(maxsize=1000)
    stop_flag = [False]
    writer = Thread(target=worker_write, args=(out_path, db, queue, cache_size), daemon=False)
    writer.start()

    # Use local input (merge downloaded file)
    if in_path is not None:
        def qlen(_):
            return '' if queue.empty() else '(%d)' % queue.qsize()

        if os.path.isdir(in_path):
            file_paths = [os.path.join(in_path, file) for file in os.listdir(in_path)]
        else:
            file_paths = [in_path]

        try:
            for file_path in file_paths:
                label = '%s\t' % file_path.split(os.sep)[-1]
                if file_path.endswith('.sqlite'):
                    from sqlitedict import SqliteDict
                    sqlite = SqliteDict(file_path, tablename='tweets', flag='r', encode=str, decode=str)
                    with click.progressbar(length=len(sqlite), show_percent=True,
                                           item_show_func=qlen, label=label) as bar:
                        for row in sqlite.values():
                            tweet = json.loads(row)
                            if no_filter or is_valid(tweet):
                                queue.put(tweet)
                            bar.update(1)
                else:
                    size = os.path.getsize(file_path)
                    with open(file_path, 'r') as fp:
                        with click.progressbar(length=size, show_percent=True,
                                               item_show_func=qlen, label=label) as bar:
                            for row in fp:
                                tweet = json.loads(row)
                                if no_filter or is_valid(tweet):
                                    queue.put(tweet)
                                bar.update(len(row))

        except KeyboardInterrupt:
            print('Interrupted!')

        queue.put(STOP_FLAG)
        if not queue.empty():
            print('Clearing pending queue...')
        return

    # Get twitter API keys
    keys = getkeys(keys_path)
    if len(keys) <= 0:
        print('There is no available keys in "%s"!' % keys_path)
        queue.put(STOP_FLAG)
        return

    # Worker threads
    stream_status = []
    search_status = []
    for key in keys:
        if key.stream_grid:
            status = WorkerStatus(key)
            stream_status.append(status)
            worker = Thread(target=worker_stream, args=(key, status, queue, no_filter), daemon=True)
            worker.start()
        if key.search_geocode:
            status = WorkerStatus(key)
            search_status.append(status)
            worker = Thread(target=worker_search, args=(key, status, queue, no_filter), daemon=True)
            worker.start()

    stream_status.sort(key=lambda s: s.key.stream_name)
    search_status.sort(key=lambda s: s.key.search_name)

    # Logging thread
    logger = Thread(target=worker_log, args=(
        log_path, stream_status, search_status, queue, db, out_path, stop_flag, not no_filter, silence), daemon=True)
    logger.start()

    # Main thread wait for exit
    wait_for_exit()

    # Finish up
    end_time = datetime.now()
    print('Terminated at %s' % str(end_time)[:-7])
    if log_path is not None:
        log_fp = open(log_path, 'a')
        log_fp.write('Terminated at %s%s' % (str(end_time)[:-7], os.linesep))
        log_fp.flush()
        log_fp.close()
    if not queue.empty():
        print('Clearing pending queue...')
    queue.put(STOP_FLAG)
    stop_flag[0] = True
    writer.join()


if __name__ == '__main__':
    main()

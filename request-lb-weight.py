#!/usr/bin/env python

# Please note the LICENSE file accompanying this script.
# See https://github.com/reincubate/haproxy-dynamic-weight for more information.

import os, socket, site, sys, redis

# If the calculation of the load AND the weighting/actioning
# of the load data is at the same interval (1 minute) then we
# will see a lot of jerkiness. So we take the 5 minute average.
# This means servers get lowered in priority more slowly.
load = os.getloadavg()[1]
hostname = socket.gethostname()
max_load = 5

if len(sys.argv) < 2:
    raise Exception( 'You must pass the hostname and port of your memcached server' )

# Weight must range from 1 - 256
if load < 0.001:
    load = 0.001
if load > max_load:
    load = max_load

weight = int( ( (255 / max_load) * ( ( max_load + 0.001 ) - load ) ) + 1 )

if len(sys.argv) > 3:
    print 'Declaring weight of %s for %s for %ss, given load of %s' % ( weight, hostname, 60 * 2, load )

r = redis.StrictRedis(host=sys.argv[1], port=sys.argv[2], db=0)
r.set( 'server-weight-%s' % hostname, weight)
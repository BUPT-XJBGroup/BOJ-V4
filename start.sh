
uwsgi --chdir=${HOME}/PycharmProjects/BOJ-V4\
    --module=bojv4.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=bojv4.settings \
    --master --pidfile=/tmp/project-master.pid \
    --socket=/tmp/oj.sock \
    --processes=4 \
    --harakiri=20 \
    --max-requests=5000 \
    --home=${HOME}/oj/ \
    --daemonize=/var/log/uwsgi/bojv4.log      # background the proces
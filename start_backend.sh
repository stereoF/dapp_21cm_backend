nohup uvicorn main:app --host 0.0.0.0 --port 8000 >> web.log 2>&1 &
nohup python event_listen.py >> listener_polygon.log 2>&1  &
nohup python event_listen_mumbai.py  >> listener_mumbai.log 2>&1 &

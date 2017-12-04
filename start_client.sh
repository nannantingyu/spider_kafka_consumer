#!/bin/bash
cd /home/nginx/crawlerConsumer && nohup python main.py -c Jin10calendar &
cd /home/nginx/crawlerConsumer && nohup python main.py -c Jin10kuaixun &
cd /home/nginx/crawlerConsumer && nohup python main.py -c Fx678calendar &
cd /home/nginx/crawlerConsumer && nohup python main.py -c Fx678kuaixun &
cd /home/nginx/crawlerConsumer && nohup python main.py -c Wallstreetcnkuaixun &
cd /home/nginx/crawlerConsumer && nohup python main.py -c Article &
cd /home/nginx/crawlerConsumer && nohup python main.py -c Filedown &

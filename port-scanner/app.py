from flask import Flask, render_template, request
import socket
import threading
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    results = []
    target = ""
    scan_time = 0
    total_ports = 0
    open_count = 0
    closed_count = 0

    if request.method == 'POST':

        target = request.form['target']

        try:
            target_ip = socket.gethostbyname(target)

            common_ports = [
20,21,22,23,25,53,67,68,69,
80,81,88,110,111,123,135,
137,138,139,143,161,162,
179,389,443,445,465,500,
514,587,636,993,995,1080,
1194,1433,1521,1723,1883,
2049,2375,2376,3306,3389,
3690,4369,5432,5672,5900,
5984,6379,6443,8000,8080,
8443,8888,9200,9300,27017,

3000,4000,5000,5601,7001,
7070,7443,8008,8081,8088,
8090,8181,8500,9000,9042,
9090,9092,9201,9418,9999,

10000,11211,15672,18080,
27018,28017,50070,50075,
61616,27019,25565,32400,
50030,50060,61613,61614,

21,22,23,25,53,80,110,135,
139,143,389,443,445,465,
587,636,993,995,1433,1521,
3306,3389,5432,5900,6379,
8080,8443,9200,27017

]
            start_time = time.time()

            lock = threading.Lock()

            def scan_port(port):

                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)

                    result = s.connect_ex((target_ip, port))

                    if result == 0:

                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "Unknown"

                        with lock:
                            results.append((port, service))

                    s.close()

                except:
                    pass

            threads = []

            for port in common_ports:

                thread = threading.Thread(
                    target=scan_port,
                    args=(port,)
                )

                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            end_time = time.time()

            scan_time = round(end_time - start_time, 2)

            total_ports = len(common_ports)
            open_count = len(results)
            closed_count = total_ports - open_count

            results.sort()

        except:
            results = [("Error", "Invalid Target")]

    return render_template(
        'index.html',
        results=results,
        target=target,
        scan_time=scan_time,
        total_ports=total_ports,
        open_count=open_count,
        closed_count=closed_count
    )

if __name__ == '__main__':
    app.run(debug=True)
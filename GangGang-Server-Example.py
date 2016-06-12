import socket
import pickle
import time
import numpy as np

def recv_timeout(the_socket , timeout=1):
    the_socket.setblocking(0)
     
    total_data=[]
    data=''
     
    begin = time.time()

    while True:
        #if you got some data, then break after timeout
        if total_data and time.time() - begin > timeout:
            break
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time() - begin > timeout * 2:
            break
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    #join all parts to make final string
    return ''.join(total_data)

def recv_unpickle(socket, custom_function):
    data = recv_timeout(socket)
    if len(data) > 0:
        try:
            process_data( pickle.loads(data) , socket, custom_function)
        except EOFError, e:
            return None

def process_data(data, socket, custom_function):

    if type(data).__name__ != 'list':
        raise TypeError('data is not a list!') 

    result = custom_function(data)
    
    socket.sendall(str(result))


def listen_and_execute(host, port, custom_function):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    while True:
        conn, addr = serversocket.accept()
        recv_unpickle(conn, custom_function)

############
############
############


def sumsum(data):

    npd = np.array(data)
    result = np.sum(npd)
    print "the total is:", result
    return result


if __name__ == "__main__":

    host = '172.16.15.1'
    port = 9091

    listen_and_execute(host, port, sumsum)



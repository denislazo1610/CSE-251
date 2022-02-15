import multiprocessing 

def sender(conn): 
    """ function to send messages to other end of pipe """
    conn.send('Hello')
    conn.send('World')
    conn.close() 			# Close this connection when done

def receiver(conn): 
    """ function to print the messages received from other end of pipe  """
    print(f'Received: {conn.recv()}')
    print(f'Received: {conn.recv()}')

    if conn.recv():
        print('there is something else')
    else:
        print('It is finished')
    

if __name__ == "__main__": 

    # creating a pipe 
    parent_conn, child_conn = multiprocessing.Pipe() 

    # creating new processes 
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,)) 
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,)) 

    # running processes 
    p1.start() 
    p2.start() 

    # wait until processes finish 
    p1.join() 
    p2.join() 
import io 

def read_socket(in_socket,size=1024):
    """
    Reads the data from the in_socket in blocks of 'size' into a BytesIO

    :param in_socket: the socket to read
    :param size: the size of the block to read
    :return: the value of the BytesIO buffer
    """

    # create the buffer
    buf = io.BytesIO()
    done = False

    while not done:
        # read the data
        data = in_socket.recv(size)
        if len(data) < size:
            done=True

        # append the data
        buf.write(data)

    return buf.getvalue()



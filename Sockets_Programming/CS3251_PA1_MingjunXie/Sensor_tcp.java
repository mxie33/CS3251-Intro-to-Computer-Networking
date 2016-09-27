import java.net.Socket;
import java.net.SocketException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Random;
public class Sensor_tcp {

  public static void main(String[] args) throws IOException {
    boolean debug = false;

    if (args.length != 10 || args.length != 11) {// Test for correct # of args
      throw new IllegalArgumentException("sensor-tcp usage: -s host name -p port number -u username -c password -r sensor value -d for debug mode");
      // throw an exception if args are not in the format
    }

    String server = args[1];
    int portNumber = Integer.parseInt(args[3]);
    String username = args[5];
    String password = args[7];
    String sensorVal = args[9];

    if (args[10] == "-d") {
        debug = true;
    }

    // if debug mode, the information will be printed out
    if (debug) {
        System.out.println("server host name:" + server);
        System.out.println("server port number:" + portNumber);
        System.out.println("username:" + username);
        System.out.println("password:" + password);        
        System.out.println("sensor value:" + sensorVal);
    }

    // Create socket that is connected to server on specified port
        Socket socket = new Socket(server, portNumber);
        System.out.println("Connected to server...sending string");        

    //need MD5 algorithm
    String challenge = "ABC" + new Random().nextInt(9999)*31%11 + 7;
    try {
        byte[] hash = new MD5().MD5ALG(username, password, challenge);
        InputStream in = socket.getInputStream();
        OutputStream out = socket.getOutputStream();
        out.write(hash);  // Send the encoded string to the server
    } catch (Exception e) {
        System.out.println("There's an error in the algorithm");
    }
 

    // Client sends "authentication request" message.
    //Server responds with a one time use, challenge value in the form of a random 64 character string. (You get to decide how this random string is generated.)
    //Client computes a MD5 hash of the string formed by concatenating the username, password and the random string sent by the server. Hash = MD5("username","password","challenge")
    //Client sends the clear text "username" and the resulting "Hash" to the server.
    //The server takes the username, finds the corresponding password on file, and performs the same MD5 calculation. It then compares the calculated Hash to the one sent by the client. 
    //If they match, the user has successfully authenticated. If no match, then authentication fails.



    // // Receive the same string back from the server
    // int totalBytesRcvd = 0;  // Total bytes received so far
    // int bytesRcvd;           // Bytes received in last read
    // while (totalBytesRcvd < data.length) {
    //   if ((bytesRcvd = in.read(data, totalBytesRcvd,  
    //                     data.length - totalBytesRcvd)) == -1)
    //     throw new SocketException("Connection closed prematurely");
    //   totalBytesRcvd += bytesRcvd;
    // }  // data array is full

    // System.out.println("Received: " + new String(data));

    socket.close();  // Close the socket and its streams
  }
}
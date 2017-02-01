import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
 
/**
 * Test MD5 digest computation
 *
 * @author Roedy Green
 * @version 1.0
 * @since 2004-06-07
 */
public final class MD5{
    public MD5() {

    }
    public static byte[] MD5ALG(String username, String password, String challenge) throws UnsupportedEncodingException,
            NoSuchAlgorithmException{
        String args = username + password + challenge;
        byte[] theTextToDigestAsBytes=
                args.getBytes("8859_1");

        MessageDigest md= MessageDigest.getInstance("MD5");
        md.update(theTextToDigestAsBytes);

        byte[] digest= md.digest();
        // dump out the hash
        for(byte b: digest){
            System.out.printf("%02X", b & 0xff);
        }
        System.out.println();
        return digest;
    }

}
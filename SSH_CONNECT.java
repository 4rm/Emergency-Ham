import java.io.InputStream;
import java.io.File;
import java.util.Scanner;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class SSH_CONNECT {


	public static void main(String[] args){
	    
	    try{
	    
		File ssh_config = new File("ssh_config");
		Scanner sc = new Scanner(ssh_config);

	    
		String host = sc.nextLine();
		String user = sc.nextLine();
		String password = sc.nextLine();
		String keypassphrase = password;
		String privatekey = sc.nextLine();
		String command1= sc.nextLine();
		sc.close();
	    

	    	
	    	java.util.Properties config = new java.util.Properties(); 
	    	config.put("StrictHostKeyChecking", "no");
	    	JSch jsch = new JSch();
	    	jsch.addIdentity(privatekey, keypassphrase);
	    	Session session=jsch.getSession(user, host, 2222);
	    	session.setPassword(password);
	    	session.setConfig(config);
	    	session.connect();
	    	
	    	Channel channel=session.openChannel("exec");
	        ((ChannelExec)channel).setCommand(command1);
	        channel.setInputStream(null);
	        ((ChannelExec)channel).setErrStream(System.err);
	        
	        InputStream in=channel.getInputStream();
	        channel.connect();
	        byte[] tmp=new byte[1024];
	        while(true){
	          while(in.available()>0){
	            int i=in.read(tmp, 0, 1024);
	            if(i<0)break;
	            System.out.print(new String(tmp, 0, i));
	          }
	          if(channel.isClosed()){
	            break;
	          }
	          try{Thread.sleep(1000);}catch(Exception ee){}
	        }
	        channel.disconnect();
	        session.disconnect();
	    }catch(Exception e){
	    	System.out.println("ERROR");
	    }

	}
}

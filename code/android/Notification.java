package com.tutor.notification;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
public class NotificationDemo extends Activity implements OnClickListener{
    
	private Context mContext;
    private Button showButton,cancelButton;
    private Notification mNotification;
    private NotificationManager mNotificationManager;
    private final static int NOTIFICATION_ID = 0x0001;
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main); 
        
        setupViews();       
    }
    //这里是初始化一些操作，可以看到onCreate()方法里代码非常简洁。
    public void setupViews(){
    	   mContext = NotificationDemo.this;
    	   showButton = (Button)findViewById(R.id.showButton);
    	   cancelButton = (Button)findViewById(R.id.cancelButton);
    	   
           mNotification = new Notification(R.drawable.icon,"This is a notification.",System.currentTimeMillis());
           //将使用默认的声音来提醒用户
           mNotification.defaults = Notification.DEFAULT_SOUND;
           mNotificationManager = (NotificationManager)this.getSystemService(NOTIFICATION_SERVICE);
           
          
           showButton.setOnClickListener(this);
           cancelButton.setOnClickListener(this);
    }
    //按钮点击事件响应
	public void onClick(View v) {
		
		if(v == showButton){
			Intent mIntent = new Intent(mContext,NotificationDemo.class);
			//这里需要设置Intent.FLAG_ACTIVITY_NEW_TASK属性
			mIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);	
			PendingIntent mContentIntent =PendingIntent.getActivity(mContext,0, mIntent, 0);
			//这里必需要用setLatestEventInfo(上下文,标题,内容,PendingIntent)不然会报错.
			mNotification.setLatestEventInfo(mContext, "10086", "您的当前话费不足,请充值.哈哈~", mContentIntent);
			//这里发送通知(消息ID,通知对象)
	        mNotificationManager.notify(NOTIFICATION_ID, mNotification);   
		}else if(v == cancelButton){
			//取消只要把通知ID传过来就OK了.
			mNotificationManager.cancel(NOTIFICATION_ID);
		}
	}
}
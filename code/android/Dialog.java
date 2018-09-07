import android.content.DialogInterface;

    AlertDialog.Builder ad = new AlertDialog.Builder(this);

    ad.setTitle("Input");
    ad.setIcon(R.drawable.tools);
    ad.setMessage("Enter your name");

    final EditText input = new EditText(this);
    ad.setView(input);

	ad.setItems(items, new DialogInterface.OnClickListener()
	{
		public void onClick(DialogInterface dialog, int which)
		{
			input.setText(items[which])
		}
	});
	
	ad.setSingleChoiceItems(items, 1, new DialogInterface.OnClickListener()
	{
		public void onClick(DialogInterface dialog, int which)
		{
			input.setText(items[which])
		}
	}
	
    ad.setPositiveButton("Ok", new DialogInterface.OnClickListener() 
    {
    	public void onClick(DialogInterface dlg, int which) 
    	{
    		String val = input.getText().toString();
    	}
    });

    ad.setNegativeButton("Cancel", new DialogInterface.OnClickListener() 
    {
    	public void onClick(DialogInterface dlg, int which) 
    	{
    		dlg.cancel();
    	}
    });
    
    TableLayout loginForm = (TableLayout)getLayoutInflater().inflate(R.layout.login, null);
    ad.setView(loginForm);
    
    ad.show();
/***
	Copyright (c) 2008-2009 CommonsWare, LLC
	
	Licensed under the Apache License, Version 2.0 (the "License"); you may
	not use this file except in compliance with the License. You may obtain
	a copy of the License at
		http://www.apache.org/licenses/LICENSE-2.0
	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
*/

package com.commonsware.android.skeleton;

import android.app.Activity;
import android.os.Bundle;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

public class RadioGroupDemo extends Activity 
{
  public TextView mTextView1;
  public RadioGroup mRadioGroup1; 
  public RadioButton mRadio1,mRadio2; 
  
  public void onCreate(Bundle savedInstanceState) 
  { 
    super.onCreate(savedInstanceState); 
    setContentView(R.layout.main); 
     
    mTextView1 = (TextView) findViewById(R.id.myTextView);
    mRadioGroup1 = (RadioGroup) findViewById(R.id.myRadioGroup);
    mRadio1 = (RadioButton) findViewById(R.id.myRadioButton1);
    mRadio2 = (RadioButton) findViewById(R.id.myRadioButton2); 
      
    mRadioGroup1.setOnCheckedChangeListener(mChangeRadio); 
  } 
   
  private RadioGroup.OnCheckedChangeListener mChangeRadio = new 
           RadioGroup.OnCheckedChangeListener()
  { 
    @Override 
    public void onCheckedChanged(RadioGroup group, int checkedId)
    { 
      // TODO Auto-generated method stub 
      if(checkedId==mRadio1.getId())
      { 
        /*把mRadio1的内容传到mTextView1*/
        mTextView1.setText(mRadio1.getText());
      } 
      else if(checkedId==mRadio2.getId()) 
      { 
        /*把mRadio2的内容传到mTextView1*/
        mTextView1.setText(mRadio2.getText()); 
      }       
    } 
  }; 
}
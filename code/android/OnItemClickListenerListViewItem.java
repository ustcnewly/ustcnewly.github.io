package com.example.listviewpopupwithadapter;

import android.content.Context;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.TextView;
import android.widget.Toast;

/*
 * Here you can control what to do next when the user selects an item
 */
public class OnItemClickListenerListViewItem implements OnItemClickListener {

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

        Context context = view.getContext();

        TextView textViewItem = ((TextView) view.findViewById(R.id.textViewItem));

        // get the clicked item name
        String listItemText = textViewItem.getText().toString();

        // get the clicked item ID
        String listItemId = textViewItem.getTag().toString();

        // just toast it
        Toast.makeText(context, "Item: " + listItemText + ", Item ID: " + listItemId, Toast.LENGTH_SHORT).show();

        ((MainActivity) context).alertDialogStores.cancel();

    }

}
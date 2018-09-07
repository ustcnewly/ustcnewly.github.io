public boolean onCreateOptionsMenu(Menu menu) {
        menu.add(0, 0, 0, "About");
        menu.add(0, 1, 1, "Quit");
        return super.onCreateOptionsMenu(menu);
    } 
    public boolean onOptionsItemSelected(MenuItem item) {
        super.onOptionsItemSelected(item);
        switch (item.getItemId()) {
        case 0:
            Toast.makeText(MenuDemo.this, "Welcome", Toast.LENGTH_LONG).show();        
        case 1:
            this.finish();
        }
        return true;
    }
function mycodeservice(req, resp){

	ClearBlade.init({request:req});
	var x = {
		// The email of the user that invokes this code service
		"userEmail": "anay.paul2@gmail.com",
		// Any parameters passed into this service
		// You can also pass in parameter using Test Parameters
		// in the Developer Console in browser
		"params": {
		  "key1":"value1",
		  "key2":"value2"
		},
		// System Key of this system
		"systemKey": "86e0fac90bcedcd5b09dcaaa8e77",
		// System Secret of this system
		"systemSecret": "86E0FAC90BB0CB99FDC09ED0F5ED01",
		// The active user token used to invoke this service
		//  "userToken": "U1hNf7o4bEXpiE4aGhb-79MQv4jH0v2U8nH5Oq_anGEjQh5kfAozv6CbDhDHA4xPwlRSkh2XeD1KhdQg6Q==",
		"userToken": "qPb-k3DOyH-8iqo3mRlRvIsfgWhcfO8rUQUf3VKeoeWwPHYyDeNwTYp5bzcYrUYb9l6nHbhFPHSL3iK9hA==",
		// is logging enabled (see [log](/Log.js) library)
		"isLogging": true,
		// User UUID of user who invoked this service
		"userid": "d6e8fac90bb2e3c6ea92b18b9039",
	}
	var updateCollection = function() {
		var collection = ClearBlade.Collection({collectionName:"MacbookProcesses"});
		var newRow = {
			pid: req['params']['pid'],
			name: req['params']['name'],
			username: req['params']['username'],
			memory_percent: req['params']['memory_percent']
		};
		var callback = function(err, data) {
			if (err) {
				resp.error(data);
			} else {
				resp.success("Data stored successfully");
			}
		};
		collection.create(newRow, callback);

	};
	var callback = function(err, data){
		if (err) {
			resp.error(data);
		}
		else {
			if (data.DATA.length === 0) {
				updateCollection();
			} else {
				resp.success({"pid": data.DATA[0].pid, "name" : data.DATA[0].name, "username": data.DATA[0].username, "memory_percent":data.DATA[0].memory_percent});
			}
		}
	};	
var q = ClearBlade.Query({collectionName:"MacbookProcesses"} );
    
q.equalTo("pid", 100);
q.equalTo("username","anaypaul");

q.fetch( callback);
	var message = "Successfully updated position!"
	resp.success(message) // Code Service terminates
}
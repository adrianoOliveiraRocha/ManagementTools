
// function ajax(url) {
// 	var xhttp = new XMLHttpRequest();
// 	xhttp.onreadystatechange = function() {
// 		if (this.readyState == 4 && this.status == 200) {
// 			    document.getElementById("central-content").innerHTML =
// 			    this.responseText;
// 			}
// 		else{
// 			document.getElementById("central-content").innerHTML = 'Carregando...';
// 		}
// 	};

// 	xhttp.open("GET", url, true);
// 	xhttp.send();

// }

function get_date(input) {
	// receive the date
	var date = input.value;
	// onle numbers
	date = date.replace(/[^\d]+/g,'');
	
	var finalDate = '';
	
	for (var i = 0, n = date.length; i < n; ++i) {
		finalDate = finalDate + date[i];
		if (finalDate.length == 2 || finalDate.length == 5) {
			finalDate = finalDate + '/';
		}
	}
	
	input.value = finalDate;
	
}

function generate_report() {
	var init = document.getElementById('inicio').value;
	var end = document.getElementById('fim').value;
	
	if (init.length !== 10 || end.length != 10) {
		alert('Por favor! preencha a data de início e fim corretamente');
	}
	else{
		var url = '/cashjournal/generate_report/' + init + '/' + end;
		window.self.location.href = url;
	}
}


function search_launch() {
	
	var init = document.getElementById('iniciosearch').value;
	var end = document.getElementById('fimsearch').value;
	
	if (init.length !== 10 || end.length != 10) {
		alert('Por favor! preencha a data de início e fim corretamente');
	}
	else{
		var url = '/cashjournal/search_launches/' + init + '/' + end;
		// window.self.location.href = url;

		var containerResponse = document.getElementById("msg-central");

		//call ajax
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				    containerResponse.innerHTML = this.responseText;
				}
			else {
				containerResponse.innerHTML = 'Carregando...';
			}
		};

		xhttp.open("GET", url, true);
		xhttp.send();
	}
}


function search_date() {
	var date = document.getElementById('date').value;
	
	if (date.length !== 10) {
		alert('Por favor! preencha o campo data corretamente');
	}
	else{
		var url = '/cashjournal/search_date/' + date;
		// window.self.location.href = url;

		var containerResponse = document.getElementById("msg-central");

		//call ajax
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				    containerResponse.innerHTML = this.responseText;
				}
			else {
				containerResponse.innerHTML = 'Carregando...';
			}
		};
		xhttp.open("GET", url, true);
		xhttp.send();
	}
}


function edit_launch(launch_id) {
	
	var url = '/cashjournal/edit_launch/' + launch_id;  

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			    document.getElementById("msg-central").innerHTML =
			    this.responseText;
			}
		else{
			document.getElementById("msg-central").innerHTML = 'Carregando...';
		}
	};

	xhttp.open("GET", url, true);
	xhttp.send();
}

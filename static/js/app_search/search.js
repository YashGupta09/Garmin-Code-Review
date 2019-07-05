function loadTable() {
	var argu = [$('input#search').val(), $('input#search1').val()];
	var _data = JSON.parse($.ajax({
		url: '/table/',
		type: 'GET',
		data: {
			'fileName': argu[0],
			'content': argu[1]
		},
		dataType: 'json',
		async: false
	}).responseText);

	if (argu.length < 3) {
		$('#table').bootstrapTable({
			pagination: true,
			columns: [{
				field: 'id',
				title: 'File Id'
			}, {
				field: 'root',
				title: 'Path'
			}, {
				field: 'fileName',
				title: 'File Name'
			}],
		});
		$('#table').bootstrapTable('load', _data);
	}
	else {
		$('#table').bootstrapTable({
			pagination: true,
			columns: [{
				field: 'searchTerm',
				title: 'Search Term'
			}, {
				field: 'root',
				title: 'Path'
			}, {
				field: 'fileName',
				title: 'File Name'
			}, {
				field: 'lineNumber',
				title: 'Line No',
				formatter: 'LineFormatter'
			}, {
				field: 'codeLine',
				title: 'Code Line',
			}],
		});
		$('#table').bootstrapTable('load', _data);
	};
};

function runLinePython(doc_id, argu) {
	var lineNums = JSON.parse($.ajax({
		url: '/view/',
		type: 'GET',
		data: {
			'doc_id': doc_id,
			'argu': argu
		},
		dataType: 'json',
		async: false,
		error: function() {
			console.log("Could not connect!");
		},
		success: function() {
			console.log("Successful");
		}
	}).responseText);
	lineNums['numbers'].forEach(num => console.log("Line number: " + num));
};

function nameFormatter(value, row) {
	return "<a href='/files/displayFilePlain/" + value + "'>Open</a>"
};

function pathFormatter(value, row) {
	return "<a href='/files/displayFilePlain/" + value + "'>Copy</a>"
};

function LineFormatter(value, row) {
	xx = "<a href='/files/displayFile/" + row.FileID + "'>" + value + "</a>"
	return xx
};

$(function() {
	console.log()

	$('#viewfile').click(function() {
		runLinePython(1, $('input#search1').val())
	});

	$('#category_form').submit(function(e) {
		e.preventDefault();
		loadTable();
	});
});
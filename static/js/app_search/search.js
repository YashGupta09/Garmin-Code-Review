$(function() {
	$('#viewfile').click(function() {
		runLinePython(1, "import")
	});

	$('#category_form').submit(function(e) {
		e.preventDefault();
		loadTable();
	});

	function loadTable() {
		var argu = [$('input#search').val(), $('input#search1').val()];
		console.log(argu[1]);
		var _data = $.parseJSON($.ajax({
			url: '/table/',
			type: 'GET',
			data: {
				'fileName': argu[0],
				'content': argu[1]
			},
			dataType: 'json',
			async: false
		}).responseText);

		console.log(_data)

		if (argu.length < 3) {
			$('#table').bootstrapTable({
				pagination: true,
				columns: [{
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
		var lineNums = $.parseJSON($.ajax({
			url: '/view/',
			type: 'POST',
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
				console.log("Line numbers are: " + lineNums);
			}
		}).responseText);
	}

	function nameFormatter(value, row) {
		return "<a href='/files/displayFilePlain/" + value + "'>Open</a>"
	};

	function pathFormatter(value, row) {
		return "<a href='/files/displayFilePlain/" + value + "'>Copy</a>"
	};

	function LineFormatter(value, row) {
		xx = "<a href='/files/displayFile/" + row.FileID + "'>" + value+ "</a>"
		return xx
	};
});
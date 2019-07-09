var $table = $('#table');
var $search = $('input#search');
var $search1 = $('input#search1');

function initTable() {
	$table.bootstrapTable({
		columns: [{
			field: 'id',
			title: 'File Id'
		}, {
			field: 'root',
			title: 'Path'
		}, {
			field: 'fileName',
			title: 'File Name',
			formatter: 'linkFormatter'
		}, {
			field: 'highlight',
			title: 'Highlight',
			formatter: 'linkFormatter'
		}]
	});
};

function loadTable() {
	var argu = [$search.val(), $search1.val()];
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

	initTable()

	//toggle highlight column depending on arguments of 2nd input
	if ($search1.val() != "")
		$table.bootstrapTable('showColumn', 'highlight');
	else
		$table.bootstrapTable('hideColumn', 'highlight');

	$table.bootstrapTable('load', _data);
};

function linkFormatter(value, row) {
	return "<a href='/view/" + row.id + "/" + $search1.val() + "/'>" + value + "</a>";
};

$(function() {
	//initialize table with no records
	initTable();
	$(".no-records-found td").html('No records to display');

	$('#category_form').submit(function(e) {
		e.preventDefault();
		loadTable();
	});
});
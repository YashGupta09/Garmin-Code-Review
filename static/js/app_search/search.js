var $table = $('#table');
var $search = $('input#search');
var $search1 = $('input#search1');
var $rootDropdown = $('#rootDropdown');

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
	var notRootPaths = notSelectedOptions();
	var _data = JSON.parse($.ajax({
		url: '/table/',
		type: 'GET',
		data: {
			'fileName': $search.val(),
			'content': $search1.val(),
			'notRootPaths': notRootPaths
		},
		dataType: 'json',
		async: false
	}).responseText);

	initTable()

	//toggle show/hide highlight column depending on arguments of 2nd input
	if ($search1.val() != "")
		$table.bootstrapTable('showColumn', 'highlight');
	else
		$table.bootstrapTable('hideColumn', 'highlight');

	$table.bootstrapTable('load', _data);
};

function linkFormatter(value, row) {
	var argu = $search1.val();
	if (argu != "")
		return "<a href='/view/" + row.id + "/" + argu + "/'>" + value + "</a>";
	else
		return "<a href='/view/" + row.id + "/'>" + value + "</a>";
};

function notSelectedOptions() {
	var notRootPaths = new Array();
	var selectedRootPaths = $rootDropdown.val();
	$.map($("#rootDropdown option") ,function(option) {
		if (!selectedRootPaths.includes(option.value))
			notRootPaths.push(option.value);
	});
	return notRootPaths;
};

$(function() {
	$('#rootDropdown').multiselect({
		includeSelectAllOption: true,
		disableIfEmpty: true,
		nonSelectedText: 'Select root path(s)',
		numberDisplayed: 1
	});

	//initialize table with no records
	initTable();
	$(".no-records-found td").html('No records to display');

	$('#category_form').submit(function(e) {
		e.preventDefault();
		loadTable();
	});
});
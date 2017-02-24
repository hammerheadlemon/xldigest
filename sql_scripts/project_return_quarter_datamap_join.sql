SELECT project.name, quarter.name, datamap_item.key, returns.value
FROM returns
	INNER JOIN datamap_item
	ON returns.datamap_id = datamap_item.datamap_item_id
	INNER JOIN project
	ON returns.project_id = project.project_id
	INNER JOIN quarter
	ON returns.quarter_id = quarter.quarter_id
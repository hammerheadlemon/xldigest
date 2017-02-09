SELECT projects.name, quarters.name, datamap_items.key, returns.value
FROM returns
	INNER JOIN datamap_items
	ON returns.datamap_item_id = datamap_items.id
	INNER JOIN projects
	ON returns.project_id = projects.id
	INNER JOIN quarters
	ON returns.quarter_id= quarters.id
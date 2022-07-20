SELECT u.id, u.firstName || ' ' || u.lastName as fullName
FROM client_wishes cw
inner join  wishes w ON w.id = cw.id_wish
inner join  users u ON u.id = cw.id_client 
where w.id = 3
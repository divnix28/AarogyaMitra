// Create Disease Node
CREATE (d:Disease {name: "Dengue", code: "DENGUE_001"})

// Create Prevention Nodes
CREATE (p1:Prevention {action: "Eliminate standing water in coolers and pots"})
CREATE (p2:Prevention {action: "Use mosquito nets and repellents"})

// Create Source Node
CREATE (s:Source {source_id: "mohfw_dengue_guidelines_2024", organization: "MoHFW"})

// Create Relationships
CREATE (d)-[:PREVENTED_BY]->(p1)
CREATE (d)-[:PREVENTED_BY]->(p2)
CREATE (d)-[:SUPPORTED_BY]->(s);
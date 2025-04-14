# link analysis

def pagerank(graph, damping_factor=0.85, epsilon=1.0e-8, max_iterations=100):
    # Initialize PageRank scores
    num_nodes = len(graph)
    pagerank_scores = {node: 1.0 / num_nodes for node in graph}

    for _ in range(max_iterations):
        new_pagerank_scores = {}
        max_diff = 0

        for node in graph:
            new_pagerank = (1 - damping_factor) / num_nodes
            for referring_page, links in graph.items():
                if node in links:
                    num_outlinks = len(links)
                    new_pagerank += damping_factor * (pagerank_scores[referring_page] / num_outlinks)

            new_pagerank_scores[node] = new_pagerank
            max_diff = max(max_diff, abs(new_pagerank - pagerank_scores[node]))

        pagerank_scores = new_pagerank_scores

        if max_diff < epsilon:
            break

    return pagerank_scores

# Create a small web graph
web_graph = {
    'A': ['B', 'C'],
    'B': ['C'],
    'C': ['A']
}

# Compute PageRank scores
pagerank_scores = pagerank(web_graph)

# Analyze the results
sorted_scores = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)

print("PageRank scores:")
for node, score in sorted_scores:
    print(f"{node}: {score:.6f}")

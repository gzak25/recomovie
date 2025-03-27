import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

def build_genre_graph(movie_dict):
    """Builds a graph where genres are nodes and edges exist if movies share genres."""
    genre_graph = {}
    for movie, details in movie_dict.items():
        # # To make the graph more sparse
        # for genre in details['genres'][1:3]:
        for genre in details['genres']:
            if genre not in genre_graph:
                genre_graph[genre] = set()
            genre_graph[genre].update(details['genres'])
            genre_graph[genre].remove(genre)
    return genre_graph

def bfs_genre_exploration(start_genre, genre_graph, max_depth):
    """Performs BFS to explore genres up to a certain depth."""
    goal_genres = []
    while not goal_genres:
        queue = deque()
        queue.append((start_genre, 0))
        explored_genres = [start_genre]
        while queue:
            current_genre, depth = queue.popleft()
            if depth == max_depth:
                goal_genres.append(current_genre)
                explored_genres.append(current_genre)
            elif depth > max_depth: 
                continue
            for neighbor in genre_graph.get(current_genre, []):
                if neighbor not in explored_genres:
                    explored_genres.append(neighbor)
                    queue.append((neighbor, depth + 1))
        if goal_genres == []:
            max_depth -= 1
    return goal_genres

def get_movie_recommendations(movie_dict, fav_movie, exploration_pct):
    if fav_movie not in movie_dict:
            print("Movie not found in database.")
            return []
        
    genre_graph = build_genre_graph(movie_dict)
    fav_genres = movie_dict[fav_movie]['genres'][0]
    
    # Define depth of exploration based on percentage
    if exploration_pct <= 25:
        max_depth = 0  # Strictly same genre
    elif exploration_pct <= 50:
        max_depth = 1  # Explore related genres
    elif exploration_pct <= 75:
        max_depth = 2  # Explore related genres
    else:
        max_depth = 3  # Broader exploration
    
    relevant_genres = bfs_genre_exploration(fav_genres, genre_graph, max_depth)
    
    # Gather movies that belong to relevant genres
    candidate_movies = []
    for movie, details in movie_dict.items():
        if movie == fav_movie:
            continue
        if any(genre in relevant_genres for genre in details['genres']):
            candidate_movies.append((movie, details['rating']))
    
    # Sort by rating
    top_movies = heapq.nlargest(5, candidate_movies, key=lambda x: x[1])
    return [(movie, rating) for movie, rating in top_movies]

def display_genre_graph(genre_graph):
    """Displays the genre graph using NetworkX and Matplotlib."""
    G = nx.Graph()
    for genre, neighbors in genre_graph.items():
        for neighbor in neighbors:
            G.add_edge(genre, neighbor)
    
    plt.figure(figsize=(10, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10, node_size=3000)
    plt.title("Genre Graph")
    plt.show()
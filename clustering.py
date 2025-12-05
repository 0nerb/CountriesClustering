import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')


def load_countries_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def prepare_clustering_data(countries):
    features = []
    countries_filtered = []
    country_names = []
    
    for country in countries:
        try:
            population_density = country.get('population_density')            
            if population_density is None:
                continue
            gini_data = country.get('gini', {})
            if not isinstance(gini_data, dict) or not gini_data:
                continue
            
            gini_value = max(gini_data.values())
            
            features.append([population_density, gini_value])
            countries_filtered.append(country)
            country_names.append(country.get('name', 'Unknown'))
        
        except (TypeError, ValueError, AttributeError):
            continue
    
    return np.array(features), countries_filtered, country_names


def perform_clustering(features, n_clusters, random_state=42):

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    clusters = kmeans.fit_predict(scaled_features)
    
    return kmeans, scaled_features, scaler, clusters


def plot_clustering(features, clusters, kmeans, scaler, country_names):

    plt.figure(figsize=(12, 8))
    
    # Gera cores para cada cluster
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    # Plota os pontos
    for i in range(len(np.unique(clusters))):
        cluster_points = features[clusters == i]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                   label=f'Cluster {i+1}', s=100, alpha=0.6, 
                   color=colors[i % len(colors)])
    
    # Plota os centroides (transformando de volta para escala original)
    centroids_scaled = kmeans.cluster_centers_
    centroids_original = scaler.inverse_transform(centroids_scaled)
    plt.scatter(centroids_original[:, 0], centroids_original[:, 1], 
               marker='X', s=500, c='black', edgecolors='white', linewidth=2,
               label='Centroides')
    
    # Configuração do gráfico
    plt.xlabel('Population Density (hab/km²)', fontsize=12, fontweight='bold')
    plt.ylabel('Gini Index', fontsize=12, fontweight='bold')
    plt.title('Clusterização: Population Density vs Gini Index', 
             fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Adiciona algumas anotações dos países nos pontos
    for idx, country_name in enumerate(country_names[:10]):  # Primeiros 10 para não poluir
        plt.annotate(country_name, 
                    (features[idx, 0], features[idx, 1]),
                    fontsize=7, alpha=0.7, 
                    xytext=(5, 5), textcoords='offset points')
    
    plt.tight_layout()
    plt.show()


def print_clustering_summary(countries_filtered, clusters, country_names):

    print("\n" + "="*60)
    print("RESUMO DA CLUSTERIZAÇÃO")
    print("="*60)
    
    for cluster_id in np.unique(clusters):
        cluster_countries = [country_names[i] for i in range(len(clusters)) if clusters[i] == cluster_id]
        print(f"\n📍 Cluster {cluster_id + 1} ({len(cluster_countries)} países):")
        for country in sorted(cluster_countries)[:5]:  
            print(f"   - {country}")
        if len(cluster_countries) > 5:
            print(f"   ... e mais {len(cluster_countries) - 5}")


def main(json_file_path, n_clusters):

    countries = load_countries_data(json_file_path)
    features, countries_filtered, country_names = prepare_clustering_data(countries)
    kmeans, scaled_features, scaler, clusters = perform_clustering(
        features, n_clusters=n_clusters
    )
    print("✓ Clusterização concluída\n")
    
    # Exibe resumo
    print_clustering_summary(countries_filtered, clusters, country_names)
    
    # Exibe gráfico
    plot_clustering(features, clusters, kmeans, scaler, country_names)


if __name__ == "__main__":
    # Caminho do arquivo JSON
    json_file = "AdjustedCountriesListOutput.json"
    
    # Executa a clusterização com 3 clusters
    main(json_file, n_clusters=4)

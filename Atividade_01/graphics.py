import csv
import os
import matplotlib.pyplot as plt

def read_costs(filepath, operator=None):
    costs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if operator is None or row.get('operator') == operator:
                costs.append(float(row['best_cost']))
    return costs

def main():
    # Caminhos para os arquivos de resultados
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, 'results')
    ga_file = os.path.join(results_dir, 'ga_raw_results.csv')
    sa_file = os.path.join(results_dir, 'sa_raw_results.csv')
    
    # Coleta os custos de cada arquivo
    ga_costs = read_costs(ga_file)
    sa_swap = read_costs(sa_file, 'create_swap_neighbor')
    sa_insertion = read_costs(sa_file, 'create_insertion_neighbor')
    sa_two_opt = read_costs(sa_file, 'create_two_opt_neighbor')
    
    # Prepara os dados para o plot
    data = [ga_costs, sa_swap, sa_insertion, sa_two_opt]
    labels = ['AG (Genético)', 'SA (Swap)', 'SA (Inserção)', 'SA (Two-Opt)']
    
    # Configuração e Criação do Boxplot
    plt.figure(figsize=(10, 6))
    
    # Estilização do boxplot
    box = plt.boxplot(data, labels=labels, patch_artist=True,
                      boxprops=dict(facecolor='#a3c1ad', color='#333333'),
                      medianprops=dict(color='red', linewidth=2),
                      whiskerprops=dict(color='#333333', linewidth=1.5),
                      capprops=dict(color='#333333', linewidth=1.5),
                      flierprops=dict(marker='o', color='#e74c3c', alpha=0.5))
    
    # Cores diferentes para destacar o Two-Opt 
    box['boxes'][3].set_facecolor('#85c1e9') 

    # Labels e Títulos formatados para artigo
    plt.title('Distribuição dos Custos Finais', fontsize=14, weight='bold')
    plt.ylabel('Custo da Melhor Rota', fontsize=12)
    plt.xlabel('Algoritmo / Operador de Vizinhança', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Salvar a imagem 
    output_path = os.path.join(results_dir, 'boxplot_custos.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f'Sucesso! Gráfico gerado e salvo em:\n{output_path}')
    
    # Mostrar na tela
    plt.show()

if __name__ == '__main__':
    main()

from flask import Flask, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import json

app = Flask(__name__)

def generate_line_plot():
    plt.figure(figsize=(8, 5))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y, 'b-', label='Sine Wave')
    plt.title('Simple Line Plot')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.grid(True)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_mni_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    mni_data = data['mni_data']
    years = mni_data['years']
    
    # Création de deux sous-graphiques
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Premier graphique : MNI en pourcentage
    ax1.plot(years, mni_data['mni_percentage'], 'g-o', linewidth=2, label='MNI %')
    ax1.fill_between(years, mni_data['mni_percentage'], alpha=0.2)
    
    # Ajout des valeurs sur les points
    for x, y in zip(years, mni_data['mni_percentage']):
        ax1.text(x, y + 0.05, f'{y}%', ha='center')
    
    # Ajout des seuils
    ax1.axhline(y=3, color='g', linestyle='--', alpha=0.5, label='Seuil excellent (3%)')
    ax1.axhline(y=2, color='r', linestyle='--', alpha=0.5, label='Seuil critique (2%)')
    
    # Ajustement des limites verticales
    ax1.set_ylim(1.5, 3.5)  # Modification de la limite inférieure à 1.5
    ax1.set_yticks(np.arange(1.5, 3.6, 0.5))  # Graduations tous les 0.5%
    
    ax1.set_title('MNI en Pourcentage des Actifs Productifs')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('MNI (%)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Deuxième graphique : Composantes en pourcentage
    width = 0.35
    x = np.arange(len(years))
    
    revenus_pct = [rev/actif*100 for rev, actif in zip(mni_data['revenus_interets'], mni_data['actifs_productifs_moyens'])]
    depenses_pct = [dep/actif*100 for dep, actif in zip(mni_data['depenses_interets'], mni_data['actifs_productifs_moyens'])]
    
    ax2.bar(x - width/2, revenus_pct, width, label='Revenus (%)', color='green', alpha=0.6)
    ax2.bar(x + width/2, depenses_pct, width, label='Dépenses (%)', color='red', alpha=0.6)
    
    # Ajout des valeurs sur les barres
    for i, v in enumerate(revenus_pct):
        ax2.text(i - width/2, v, f'{v:.1f}%', ha='center', va='bottom')
    for i, v in enumerate(depenses_pct):
        ax2.text(i + width/2, v, f'{v:.1f}%', ha='center', va='bottom')
    
    ax2.set_title('Composantes de la MNI en % des Actifs')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('Pourcentage (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.legend()
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_eve_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    eve_data = data['eve_data']
    years = eve_data['years']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Premier graphique : Valeur économique selon les scénarios
    ax1.plot(years, eve_data['scenarios']['baseline'], 'g-o', label='Baseline', linewidth=2)
    ax1.plot(years, eve_data['scenarios']['up_200bps'], 'r--o', label='+200bps', linewidth=2)
    ax1.plot(years, eve_data['scenarios']['down_200bps'], 'b--o', label='-200bps', linewidth=2)
    
    ax1.set_title('Évolution de l\'EVE selon les scénarios')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('Valeur Économique (Mrd €)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Deuxième graphique : Impact des chocs de taux
    width = 0.35
    x = np.arange(len(years))
    
    ax2.bar(x - width/2, eve_data['impact']['up_200bps'], width, label='+200bps', color='red', alpha=0.6)
    ax2.bar(x + width/2, eve_data['impact']['down_200bps'], width, label='-200bps', color='blue', alpha=0.6)
    
    ax2.set_title('Impact des variations de taux sur l\'EVE')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('Impact (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_gap_taux_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    gap_data = data['gap_taux_data']
    years = gap_data['years']
    
    plt.figure(figsize=(15, 6))
    
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    
    # Premier graphique : Evolution du GAP
    gap_values = [sum(values[i] for values in gap_data['actifs_sensibles'].values()) - 
                 sum(values[i] for values in gap_data['passifs_sensibles'].values())
                 for i in range(len(years))]
    
    line = ax1.plot(years, gap_values, 'b-o', linewidth=2, label='GAP de taux')
    
    # Ajout des valeurs sur les points
    for x, y in zip(years, gap_values):
        ax1.annotate(f'{y:.0f}', (x, y), textcoords="offset points", 
                    xytext=(0,7), ha='center', color='blue')
    
    ax1.set_title('Évolution du GAP de taux')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('Milliards €')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Deuxième graphique : Composition
    width = 0.35
    x = np.arange(len(years))
    
    actifs_totaux = [sum(values[i] for values in gap_data['actifs_sensibles'].values()) 
                     for i in range(len(years))]
    passifs_totaux = [sum(values[i] for values in gap_data['passifs_sensibles'].values()) 
                      for i in range(len(years))]
    
    ax2.bar(x - width/2, actifs_totaux, width, label='Actifs sensibles', color='green', alpha=0.6)
    ax2.bar(x + width/2, passifs_totaux, width, label='Passifs sensibles', color='red', alpha=0.6)
    
    # Ajustement des limites verticales
    ax2.set_ylim(500, max(max(actifs_totaux), max(passifs_totaux)) * 1.1)
    
    ax2.set_title('Composition des éléments sensibles aux taux')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('Milliards €')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9, wspace=0.25)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_gap_liquidite_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    gap_data = data['gap_liquidite_data']
    years = gap_data['years']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Premier graphique : GAP par période
    for periode in gap_data['periodes']:
        ax1.plot(years, gap_data['gaps_par_periode'][periode], 
                marker='o', label=f'GAP {periode}')
    
    ax1.set_title('GAP de Liquidité par Période')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('GAP (Milliards €)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Deuxième graphique : Entrées et Sorties
    width = 0.35
    x = np.arange(len(years))
    
    entrees_totales = [sum(values[i] for values in gap_data['entrees_prevues'].values()) 
                      for i in range(len(years))]
    sorties_totales = [sum(values[i] for values in gap_data['sorties_prevues'].values()) 
                      for i in range(len(years))]
    
    ax2.bar(x - width/2, entrees_totales, width, label='Entrées', color='green', alpha=0.6)
    ax2.bar(x + width/2, sorties_totales, width, label='Sorties', color='red', alpha=0.6)
    
    # Ajout des valeurs sur les barres
    for i, v in enumerate(entrees_totales):
        ax2.text(i - width/2, v, f'{v:.0f}M€', ha='center', va='bottom')
    for i, v in enumerate(sorties_totales):
        ax2.text(i + width/2, v, f'{v:.0f}M€', ha='center', va='bottom')
    
    # Modification de la limite inférieure de l'axe y
    ax2.set_ylim(300, max(max(entrees_totales), max(sorties_totales)) * 1.1)
    
    ax2.set_title('Entrées et Sorties de Trésorerie')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('Milliards €')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.legend()
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_lcr_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    lcr_data = data['lcr_data']
    years = lcr_data['years']
    
    plt.figure(figsize=(15, 6))
    
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    
    # Premier graphique : Evolution du LCR
    lcr_values = [125.5, 127.8, 128.4, 129.2, 130.1]
    line = ax1.plot(years, lcr_values, 'g-o', linewidth=2, label='LCR')
    ax1.axhline(y=100, color='r', linestyle='--', alpha=0.5, label='Minimum réglementaire (100%)')
    
    # Ajout des valeurs sur les points
    for x, y in zip(years, lcr_values):
        ax1.annotate(f'{y}%', (x, y), textcoords="offset points", 
                    xytext=(0,7), ha='center', color='green')
    
    # Ajustement des limites verticales pour un meilleur centrage
    ax1.set_ylim(95, 135)  # Élargissement de l'échelle
    ax1.set_yticks(np.arange(95, 136, 5))  # Graduations tous les 5%
    
    ax1.set_title('Évolution du Liquidity Coverage Ratio')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('LCR (%)')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='lower right')
    
    # Deuxième graphique : Composition
    width = 0.35
    x = np.arange(len(years))
    
    actifs_liquides = [700, 720, 740, 760, 780]
    sorties_nettes = [650, 670, 680, 700, 720]
    
    ax2.bar(x - width/2, actifs_liquides, width, label='Actifs liquides', color='green', alpha=0.6)
    ax2.bar(x + width/2, sorties_nettes, width, label='Sorties nettes', color='red', alpha=0.6)
    
    # Ajustement des limites verticales
    ax2.set_ylim(0, 900)  # Ajusté pour mieux centrer les barres
    
    ax2.set_title('Composition du LCR')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('Milliards €')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Ajustement fin des marges
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9, wspace=0.25)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_nsfr_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    nsfr_data = data['nsfr_data']
    years = nsfr_data['years']
    
    plt.figure(figsize=(15, 6))
    
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    
    # Premier graphique : Evolution du NSFR
    nsfr_values = [115.2, 116.5, 117.1, 117.8, 118.4]
    line = ax1.plot(years, nsfr_values, 'g-o', linewidth=2, label='NSFR')
    ax1.axhline(y=100, color='r', linestyle='--', alpha=0.5, label='Minimum réglementaire')
    
    # Ajout des valeurs sur les points
    for x, y in zip(years, nsfr_values):
        ax1.annotate(f'{y}%', (x, y), textcoords="offset points", 
                    xytext=(0,7), ha='center', color='green')
    
    # Ajustement des limites verticales pour un meilleur centrage
    ax1.set_ylim(90, 125)  # Élargissement de l'échelle pour mieux centrer
    ax1.set_yticks(np.arange(90, 126, 5))  # Graduations tous les 5%
    
    ax1.set_title('Évolution du NSFR')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('NSFR (%)')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='lower right')  # Déplacement de la légende
    
    # Deuxième graphique : Composition
    width = 0.35
    x = np.arange(len(years))
    
    disponible_total = [1450, 1480, 1500, 1520, 1580]
    requis_total = [1350, 1380, 1420, 1450, 1480]
    
    ax2.bar(x - width/2, disponible_total, width, label='Financement disponible', color='green', alpha=0.6)
    ax2.bar(x + width/2, requis_total, width, label='Financement requis', color='orange', alpha=0.6)
    
    # Ajustement des limites verticales
    ax2.set_ylim(1000, 1800)
    
    ax2.set_title('Composition du NSFR')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('Milliards €')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Ajustement fin des marges
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9, wspace=0.25)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_gap_combine_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    gap_taux = data['gap_taux_data']
    gap_liq = data['gap_liquidite_data']
    years = gap_taux['years']
    
    # Création de la figure avec des marges ajustées
    plt.figure(figsize=(15, 7))
    
    # Création des sous-graphiques avec des positions spécifiques
    ax1 = plt.subplot2grid((1, 2), (0, 0), fig=plt.gcf())
    ax2 = plt.subplot2grid((1, 2), (0, 1), fig=plt.gcf())
    
    # Premier graphique : Evolution temporelle
    gap_taux_values = [80, 90, 90, 95, 100]
    gap_liq_values = [80, 85, 87, 90, 92]
    
    line1 = ax1.plot(years, gap_taux_values, 'b-o', label='GAP Taux', linewidth=2)
    line2 = ax1.plot(years, gap_liq_values, 'g-o', label='GAP Liquidité', linewidth=2)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    # Ajustement des limites verticales pour le premier graphique
    ax1.set_ylim(0, 110)  # Ajusté pour centrer les courbes
    
    # Ajout des valeurs sur les points avec des couleurs correspondantes
    for x, y1, y2 in zip(years, gap_taux_values, gap_liq_values):
        ax1.annotate(f'{y1}', (x, y1), textcoords="offset points", 
                    xytext=(0,10), ha='center', color='blue')
        ax1.annotate(f'{y2}', (x, y2), textcoords="offset points", 
                    xytext=(0,-15), ha='center', color='green')
    
    ax1.set_title('Évolution des GAPs', pad=20)
    ax1.set_xlabel('Années')
    ax1.set_ylabel('Milliards €')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')
    
    # Deuxième graphique : Matrice de risque
    scatter = ax2.scatter(gap_taux_values, gap_liq_values, 
                         c=range(len(years)), cmap='YlOrRd', s=100)
    
    # Ajout des années sur les points
    for i, (x, y) in enumerate(zip(gap_taux_values, gap_liq_values)):
        ax2.annotate(str(years[i]), (x, y), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    
    # Ajustement des limites pour le deuxième graphique
    ax2.set_xlim(75, 105)
    ax2.set_ylim(75, 95)
    
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    
    ax2.set_title('Matrice Taux/Liquidité', pad=20)
    ax2.set_xlabel('GAP Taux (Mrd €)')
    ax2.set_ylabel('GAP Liquidité (Mrd €)')
    ax2.grid(True, alpha=0.3)
    
    # Ajustement fin des marges
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9, wspace=0.25, hspace=0.2)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def generate_position_change_plot():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    change_data = data['position_change_data']
    years = change_data['years']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    colors = {'USD': '#2ecc71', 'GBP': '#3498db', 'JPY': '#e74c3c'}
    
    # Premier graphique : Position nette par devise
    for devise, values in change_data['devises'].items():
        position_nette = [(a - p)/1000 for a, p in zip(values['actifs'], values['passifs'])]
        ax1.plot(years, position_nette, marker='o', label=devise, color=colors[devise], linewidth=2)
        
        # Ajout des valeurs sur les points
        for x, y in zip(years, position_nette):
            ax1.text(x, y + (0.5 if y >= 0 else -0.5), f'{y:.1f}', ha='center')
    
    # Ajout des zones de risque avec transparence
    ax1.axhspan(15, 30, color='red', alpha=0.1, label='Zone de risque élevé')
    ax1.axhspan(-30, -15, color='red', alpha=0.1)
    
    ax1.set_title('Position Nette par Devise')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('Position Nette (Millions devise)')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')
    
    # Ajuster les limites de l'axe y pour une meilleure visualisation
    ax1.set_ylim(-35, 35)
    
    # Deuxième graphique : Exposition en EUR
    for devise, values in change_data['devises'].items():
        position_nette = (values['actifs'][-1] - values['passifs'][-1]) / values['taux_change'][-1]
        exposition_eur = position_nette / 1000
        ax2.bar(devise, exposition_eur, alpha=0.6, color=colors[devise])
        # Ajout des valeurs sur les barres
        ax2.text(devise, exposition_eur, f'{exposition_eur:.1f}M€', 
                ha='center', va='bottom')
    
    ax2.set_title('Exposition en EUR (2023)')
    ax2.set_ylabel('Millions EUR')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

@app.route('/')
def home():
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    plots = {
        'mni_plot': generate_mni_plot(),
        'eve_plot': generate_eve_plot(),
        'gap_taux_plot': generate_gap_taux_plot(),
        'gap_liquidite_plot': generate_gap_liquidite_plot(),
        'lcr_plot': generate_lcr_plot(),
        'nsfr_plot': generate_nsfr_plot(),
        'gap_combine_plot': generate_gap_combine_plot(),
        'position_change_plot': generate_position_change_plot()
    }
    return render_template('index.html', plots=plots, eve_data=data['eve_data'])

if __name__ == '__main__':
    app.run(debug=True, port=9000)

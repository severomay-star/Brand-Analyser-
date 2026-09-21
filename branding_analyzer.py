"""
===============================================================================
BRANDING ANALYZER — Módulo de Análise Científica de Branding
Versão com Gráficos, Teoria e Google Trends
===============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. SCORE PONDERADO
# =============================================================================

def obter_pesos(segmento: str = 'musica') -> Dict:
    """Retorna os pesos para cada variável baseado no segmento."""
    
    if segmento == 'musica':
        return {
            'v1': 1.5,
            'v2': 1.2,
            'v3': 1.3,
            'v4': 0.8,
            'v5': 1.0,
            'v6': 0.7,
            'v7': 0.8
        }
    elif segmento == 'contabilidade':
        return {
            'v1': 1.3,
            'v2': 1.0,
            'v3': 1.5,
            'v4': 0.6,
            'v5': 1.0,
            'v6': 0.8,
            'v7': 0.7
        }
    else:
        return {f'v{i}': 1.0 for i in range(1, 8)}


def calcular_score_ponderado(notas: Dict, segmento: str = 'musica') -> Dict:
    """Calcula score total com pesos diferenciados."""
    
    pesos = obter_pesos(segmento)
    
    score_simples = sum(notas.values()) / len(notas)
    
    soma_ponderada = sum(notas[k] * pesos.get(k, 1.0) for k in notas.keys())
    soma_pesos = sum(pesos.get(k, 1.0) for k in notas.keys())
    score_ponderado = soma_ponderada / soma_pesos
    
    breakdown = {}
    for k, nota in notas.items():
        peso = pesos.get(k, 1.0)
        contribuicao = (nota * peso) / soma_pesos
        nome = {
            'v1': 'Posicionamento',
            'v2': 'Consistência',
            'v3': 'Autoridade',
            'v4': 'Engajamento',
            'v5': 'Preço-Percepção',
            'v6': 'Onipresença',
            'v7': 'Coerência Visual'
        }.get(k, k.upper())
        
        breakdown[nome] = {
            'codigo': k.upper(),
            'nota': nota,
            'peso': peso,
            'contribuicao': round(contribuicao, 2),
            'percentual': round((contribuicao / score_ponderado * 100), 1) if score_ponderado > 0 else 0
        }
    
    if score_ponderado >= 8.0:
        classificacao = "Premium"
    elif score_ponderado >= 6.5:
        classificacao = "Forte"
    elif score_ponderado >= 5.0:
        classificacao = "Intermediária"
    else:
        classificacao = "Em Risco"
    
    return {
        'score_simples': round(score_simples, 2),
        'score_ponderado': round(score_ponderado, 2),
        'classificacao': classificacao,
        'breakdown': breakdown
    }


# =============================================================================
# 2. CLASSIFICAÇÃO DA MARCA
# =============================================================================

def classificar_marca(dados_marca: Dict, segmento: str = 'musica') -> Dict:
    """Classifica marca como Sucesso, Intermediário ou Não decolou."""
    
    score = dados_marca.get('score_total', 0)
    seguidores = dados_marca.get('seguidores', 0)
    crescimento = dados_marca.get('crescimento_mensal', 0)
    produtos = dados_marca.get('produtos_ativos', 0)
    canais = dados_marca.get('canais_ativos', 1)
    autoridade = dados_marca.get('autoridade_externa', False)
    
    if segmento == 'musica':
        THRESHOLD_SEGUIDORES = 10000
        THRESHOLD_CRESCIMENTO = 5.0
    else:
        THRESHOLD_SEGUIDORES = 50000
        THRESHOLD_CRESCIMENTO = 3.0
    
    criterios = []
    
    if score >= 7.0:
        criterios.append(f"Score alto ({score:.1f}/10)")
    if seguidores >= THRESHOLD_SEGUIDORES:
        criterios.append(f"Base relevante ({seguidores:,} seguidores)")
    if crescimento >= THRESHOLD_CRESCIMENTO:
        criterios.append(f"Crescimento consistente ({crescimento:.1f}%/mês)")
    if produtos >= 2:
        criterios.append(f"{produtos} produtos/serviços ativos")
    if canais >= 3:
        criterios.append(f"Multi-canal ({canais} canais)")
    if autoridade:
        criterios.append("Autoridade externa validada")
    
    n_criterios = len(criterios)
    
    if n_criterios >= 4:
        classificacao = "Sucesso"
        nivel = "Consolidado"
        acao = "Manter e escalar"
    elif n_criterios >= 2:
        classificacao = "Intermediário"
        nivel = "Em desenvolvimento"
        acao = "Fortalecer pontos fracos"
    else:
        classificacao = "Não decolou"
        nivel = "Inicial ou estagnado"
        acao = "Diagnóstico completo necessário"
    
    return {
        'classificacao': classificacao,
        'nivel': nivel,
        'acao_recomendada': acao,
        'criterios_atendidos': n_criterios,
        'total_criterios': 6,
        'evidencias': criterios
    }


# =============================================================================
# 3. DICAS DE ARQUÉTIPO
# =============================================================================

def dicas_arquétipo(arquétipo: str) -> Dict:
    """Retorna dicas de posicionamento para cada arquétipo."""
    
    dicas = {
        "Sábio": {
            "posicionamento": "Posicione-se como autoridade no assunto. Use dados, estatísticas e referências acadêmicas.",
            "conteudo": "Crie tutoriais detalhados, análises aprofundadas, séries educativas.",
            "linguagem": "Tom ensinativo e acessível. Use frases como 'Estudos mostram que...'",
            "visual": "Fundo neutro e profissional. Use gráficos e cores sóbrias.",
            "cta": "Aprenda comigo | Descubra o método | Domine a técnica"
        },
        "Herói": {
            "posicionamento": "Posicione-se como alguém que superou desafios e ajuda outros a fazer o mesmo.",
            "conteudo": "Mostre jornadas de superação, histórias de antes/depois, conquistas.",
            "linguagem": "Tom motivacional e inspirador. Use frases como 'Você também pode...'",
            "visual": "Cores fortes (vermelho, laranja, preto). Imagens de ação.",
            "cta": "Transforme sua vida | Supere seus limites | Comece sua jornada"
        },
        "Mago": {
            "posicionamento": "Posicione-se como alguém que revela segredos e transforma vidas.",
            "conteudo": "Mostre transformações, 'antes e depois', revelações surpreendentes.",
            "linguagem": "Tom misterioso e transformador. Use 'Descubra o segredo...'",
            "visual": "Cores profundas (roxo, azul escuro, dourado).",
            "cta": "Revele seu potencial | Transforme sua realidade"
        },
        "Fora-da-lei": {
            "posicionamento": "Posicione-se como alguém que quebra regras e faz do seu jeito.",
            "conteudo": "Mostre como você faz diferente, critique o mercado.",
            "linguagem": "Tom direto, sem filtro, provocador.",
            "visual": "Cores fortes e contrastantes (preto, vermelho, amarelo).",
            "cta": "Faça do seu jeito | Quebre as regras | Seja diferente"
        },
        "Criador": {
            "posicionamento": "Posicione-se como alguém que cria algo novo e original.",
            "conteudo": "Mostre o processo criativo, bastidores, itens exclusivos.",
            "linguagem": "Tom inspirador e inovador. Use 'Crie algo novo...'",
            "visual": "Cores vibrantes e variadas. Mostre criação e originalidade.",
            "cta": "Crie algo incrível | Dê vida às suas ideias"
        },
        "Governante": {
            "posicionamento": "Posicione-se como uma autoridade que traz ordem e estrutura.",
            "conteudo": "Mostre sistemas, metodologias, processos organizados.",
            "linguagem": "Tom de autoridade, confiável. Use 'Com nosso método...'",
            "visual": "Cores sóbrias e elegantes (azul marinho, cinza, dourado).",
            "cta": "Organize sua vida | Domine o processo | Tenha controle"
        },
        "Cuidador": {
            "posicionamento": "Posicione-se como alguém que acolhe, cuida e protege.",
            "conteudo": "Mostre histórias emocionantes, depoimentos de superação.",
            "linguagem": "Tom afetuoso, empático. Use 'Você não está sozinho...'",
            "visual": "Cores suaves (azul claro, verde, bege).",
            "cta": "Cuide de você | Encontre seu caminho | Seja acolhido"
        },
        "Explorador": {
            "posicionamento": "Posicione-se como alguém que descobre, explora e traz novidades.",
            "conteudo": "Mostre viagens, descobertas, tendências, novidades.",
            "linguagem": "Tom aventureiro, curioso. Use 'Descubra...', 'Explore...'",
            "visual": "Cores vibrantes (verde, laranja, azul turquesa).",
            "cta": "Explore novas possibilidades | Aventure-se"
        },
        "Amante": {
            "posicionamento": "Posicione-se como alguém que vive com paixão e intensidade.",
            "conteudo": "Mostre estética refinada, experiências sensoriais.",
            "linguagem": "Tom apaixonado e envolvente. Use 'Sinta a paixão...'",
            "visual": "Cores quentes e elegantes (vermelho, vinho, rosa, dourado).",
            "cta": "Viva sua paixão | Sinta a diferença | Entregue-se"
        },
        "Bobo da Corte": {
            "posicionamento": "Posicione-se como alguém que traz leveza, humor e diversão.",
            "conteudo": "Memes, paródias, sátiras do mercado, humor inteligente.",
            "linguagem": "Tom irreverente, engraçado e leve.",
            "visual": "Cores alegres (amarelo, laranja, rosa).",
            "cta": "Divirta-se | Relaxe | Leve a vida mais leve"
        },
        "Cara Comum": {
            "posicionamento": "Posicione-se como uma pessoa comum, acessível e autêntica.",
            "conteudo": "Mostre seu dia a dia, desafios reais, linguagem simples.",
            "linguagem": "Tom acessível, autêntico e próximo.",
            "visual": "Cores neutras e naturais.",
            "cta": "Seja autêntico | Simplifique"
        },
        "Inocente": {
            "posicionamento": "Posicione-se como alguém que vê o melhor no mundo.",
            "conteudo": "Conteúdo positivo, inspirador, mensagens de esperança.",
            "linguagem": "Tom otimista, puro e inspirador.",
            "visual": "Cores claras e suaves (branco, azul céu, rosa claro).",
            "cta": "Acredite no melhor | Confie no processo | Seja leve"
        }
    }
    
    return dicas.get(arquétipo, None)


# =============================================================================
# 4. RECOMENDAÇÕES AUTOMATIZADAS
# =============================================================================

def _dicas_arquétipo_simples(arquétipo: str) -> str:
    """Retorna dicas de comunicação para cada arquétipo (versão simples)."""
    dicas = {
        'Sábio': "Use dados, estatísticas e referências acadêmicas.",
        'Herói': "Mostre desafios superados. Use narrativa de jornada do herói.",
        'Mago': "Use linguagem de transformação.",
        'Fora-da-lei': "Seja provocador, quebre regras.",
        'Criador': "Mostre o processo criativo.",
        'Governante': "Use linguagem de autoridade.",
        'Cuidador': "Mostre empatia e acolhimento.",
        'Explorador': "Mostre descobertas e novidades.",
        'Amante': "Use estética refinada.",
        'Bobo da Corte': "Use humor e leveza.",
        'Cara Comum': "Use linguagem acessível.",
        'Inocente': "Use otimismo e simplicidade."
    }
    return dicas.get(arquétipo, "Pesquise sobre o arquétipo.")


def gerar_recomendacoes(notas: Dict, arquétipo: Optional[str] = None) -> Dict:
    """Gera recomendações baseadas nas notas."""
    
    mapa = {
        'v1': {
            'baixo': "Defina um nicho mais específico: [público] + [problema] + [solução].",
            'medio': "Refine seu nicho. Pesquise concorrentes e identifique um ângulo único.",
            'alto': "Mantenha e aprofunde. Crie conteúdo que reforce sua posição."
        },
        'v2': {
            'baixo': "Crie um calendário editorial com 3 posts/semana por 3 meses.",
            'medio': "Aumente a frequência para 4-5 posts/semana.",
            'alto': "Mantenha a consistência. Considere séries temáticas."
        },
        'v3': {
            'baixo': "Documente resultados. Crie um portfólio de casos.",
            'medio': "Busque depoimentos em vídeo. Publique resultados específicos.",
            'alto': "Busque validação externa (prêmios, mídia, parcerias)."
        },
        'v4': {
            'baixo': "Faça perguntas abertas. Responda todos os comentários.",
            'medio': "Crie conteúdos que gerem debate. Faça enquetes.",
            'alto': "Incentive UGC. Crie uma hashtag oficial."
        },
        'v5': {
            'baixo': "Reveja seu preço. Pesquise concorrentes e ajuste.",
            'medio': "Comunique o valor antes do preço.",
            'alto': "Considere aumentar o preço para reforçar percepção premium."
        },
        'v6': {
            'baixo': "Escolha 1 canal principal e domine. Publique 5x/semana.",
            'medio': "Expanda para um segundo canal.",
            'alto': "Mapeie todos os pontos de contato do cliente."
        },
        'v7': {
            'baixo': "Defina paleta de cores e cenário fixo.",
            'medio': "Padronize: mesma iluminação, mesmo fundo.",
            'alto': "Crie elementos visuais exclusivos."
        }
    }
    
    recomendacoes = {'criticas': [], 'importantes': [], 'otimizacoes': []}
    
    for var, nota in notas.items():
        if var in mapa:
            if nota < 5:
                recomendacoes['criticas'].append({
                    'variavel': var.upper(),
                    'nota': nota,
                    'recomendacao': mapa[var]['baixo']
                })
            elif nota < 7:
                recomendacoes['importantes'].append({
                    'variavel': var.upper(),
                    'nota': nota,
                    'recomendacao': mapa[var]['medio']
                })
            else:
                recomendacoes['otimizacoes'].append({
                    'variavel': var.upper(),
                    'nota': nota,
                    'recomendacao': mapa[var]['alto']
                })
    
    if arquétipo:
        recomendacoes['arquétipo'] = {
            'atual': arquétipo,
            'dicas': _dicas_arquétipo_simples(arquétipo),
            'acao': f"Reforce o arquétipo {arquétipo} na comunicação."
        }
    
    n_criticas = len(recomendacoes['criticas'])
    n_importantes = len(recomendacoes['importantes'])
    
    if n_criticas > 0:
        resumo = f"⚠️ {n_criticas} pontos críticos precisam de atenção imediata."
    elif n_importantes > 0:
        resumo = f"📈 {n_importantes} áreas para melhoria identificadas."
    else:
        resumo = "✅ Marca bem estruturada. Foco em otimizações."
    
    recomendacoes['resumo'] = resumo
    
    return recomendacoes


# =============================================================================
# 5. ANÁLISE DE POSICIONAMENTO VIA TRANSCRIÇÃO (V1)
# =============================================================================

def analisar_posicionamento_v1(bio: str, transcricoes: list) -> dict:
    """Analisa o posicionamento da marca com base na bio e transcrições."""
    
    nichos = {
        'guitarra': {
            'palavras': ['guitarra', 'violão', 'corda', 'solo', 'acorde', 'riff', 'cifra', 'dedilhado', 'palheta'],
            'especificidade': 1,
            'subnichos': {
                'slide': ['slide', 'slide guitar', 'bottleneck', 'blues slide', 'copo', 'garrafa'],
                'blues': ['blues', 'blue', '12 compassos', 'pentatônica'],
                'rock': ['rock', 'roque', 'distorção', 'overdrive', 'solo de rock'],
                'jazz': ['jazz', 'harmonia', 'acordes estendidos', 'improvisação'],
                'fingerstyle': ['fingerstyle', 'dedilhado', 'violão dedilhado', 'tapping'],
                'iniciante': ['iniciante', 'começando', 'primeiros passos', 'zero', 'básico'],
                'intermediario': ['intermediário', 'avançando', 'próximo nível', 'técnica'],
                'avancado': ['avançado', 'profissional', 'virtuose', 'técnica avançada']
            }
        },
        'canto': {
            'palavras': ['voz', 'cantar', 'canto', 'afinação', 'técnica vocal', 'respiração', 'coral', 'performance', 'timbre'],
            'especificidade': 1,
            'subnichos': {
                'tecnica_vocal': ['técnica vocal', 'exercício vocal', 'aquecimento', 'registro', 'falsete'],
                'performance': ['performance', 'palco', 'show', 'apresentação', 'interpretação'],
                'coral': ['coral', 'coro', 'harmonia vocal', 'arranjo vocal'],
                'iniciante': ['iniciante', 'começando', 'primeiros passos', 'zero', 'básico'],
                'profissional': ['profissional', 'avançado', 'estúdio', 'gravação']
            }
        },
        'contabilidade': {
            'palavras': ['imposto', 'declaração', 'irpf', 'contábil', 'empresa', 'dfe', 'nota fiscal', 'fiscal', 'tributário', 'contador', 'balanço'],
            'especificidade': 1,
            'subnichos': {
                'pessoa_fisica': ['pf', 'pessoa física', 'declaração irpf', 'imposto de renda', 'carnê leão', 'ajuste', 'restituição'],
                'pessoa_juridica': ['pj', 'pessoa jurídica', 'empresa', 'mei', 'simples nacional', 'lucro presumido', 'lucro real'],
                'tributario': ['tributário', 'tributos', 'impostos', 'elaboração fiscal', 'planejamento tributário', 'reforma tributária'],
                'trabalhista': ['trabalhista', 'funcionário', 'folha de pagamento', 'encargos', 'rescisão', 'clt'],
                'digital': ['digital', 'contabilidade digital', 'sistema', 'automação', 'software', 'cloud'],
                'reforma_tributaria': ['reforma tributária', 'nova reforma', 'emenda', 'proposta de emenda', 'pós-reforma', 'impactos da reforma'],
                'mei': ['mei', 'microempreendedor', 'individual', 'simples', 'documentação', 'formalização'],
                'agronegocio': ['agro', 'agronegócio', 'rural', 'produtor rural', 'funrural', 'senar']
            }
        },
        'slide_guitar': {
            'palavras': ['slide', 'slide guitar', 'bottleneck', 'blues slide', 'copo', 'garrafa'],
            'especificidade': 3,
            'subnichos': {}
        },
        'marketing': {
            'palavras': ['marketing', 'vendas', 'tráfego', 'conversão', 'lead', 'campanha', 'anúncio', 'funil', 'branding'],
            'especificidade': 1,
            'subnichos': {
                'digital': ['digital', 'tráfego pago', 'facebook ads', 'instagram ads', 'google ads'],
                'conteudo': ['conteúdo', 'blog', 'copywriting', 'seo', 'email marketing', 'newsletter'],
                'vendas': ['vendas', 'funil de vendas', 'fechamento', 'negociação', 'prospecção']
            }
        },
        'empreendedorismo': {
            'palavras': ['empreender', 'negócio', 'startup', 'empresário', 'gestão', 'liderança', 'planejamento'],
            'especificidade': 1,
            'subnichos': {
                'startup': ['startup', 'scaleup', 'vc', 'venture capital', 'aceleração'],
                'pequena_empresa': ['pequena empresa', 'mei', 'microempreendedor', 'negócio local'],
                'gestao': ['gestão', 'administração', 'processos', 'indicadores', 'kpi']
            }
        },
        'saude': {
            'palavras': ['saúde', 'bem-estar', 'nutrição', 'exercício', 'mental', 'meditação', 'alimentação', 'fitness'],
            'especificidade': 1,
            'subnichos': {
                'nutricao': ['nutrição', 'nutri', 'alimentação', 'dieta', 'receita', 'saudável', 'macro', 'caloria'],
                'fitness': ['musculação', 'academia', 'treino', 'personal', 'hipertrofia', 'emagrecimento', 'pilates', 'yoga'],
                'saude_mental': ['saúde mental', 'ansiedade', 'estresse', 'meditação', 'mindfulness', 'terapia']
            }
        }
    }
    
    temas = {}
    todos_textos = ' '.join(transcricoes).lower()
    
    for nicho, dados in nichos.items():
        contagem = 0
        for palavra in dados['palavras']:
            if palavra.lower() in todos_textos:
                contagem += todos_textos.count(palavra.lower())
        if contagem > 0:
            temas[nicho] = contagem
    
    nicho_principal = max(temas, key=temas.get) if temas else None
    
    subnichos_encontrados = []
    if nicho_principal and nicho_principal in nichos:
        subnichos = nichos[nicho_principal].get('subnichos', {})
        for subnicho, palavras in subnichos.items():
            for palavra in palavras:
                if palavra.lower() in todos_textos:
                    subnichos_encontrados.append(subnicho)
                    break
    
    especificidade = 1
    if nicho_principal and nicho_principal in nichos:
        especificidade = nichos[nicho_principal].get('especificidade', 1)
    
    if subnichos_encontrados:
        especificidade += 0.5 * len(subnichos_encontrados)
    
    especificidade = min(3, especificidade)
    
    total_posts = len(transcricoes)
    posts_sobre_nicho = 0
    
    if nicho_principal and nicho_principal in nichos:
        palavras_nicho = nichos[nicho_principal]['palavras']
        for post in transcricoes:
            post_lower = post.lower()
            for palavra in palavras_nicho:
                if palavra.lower() in post_lower:
                    posts_sobre_nicho += 1
                    break
    
    coerencia = (posts_sobre_nicho / total_posts) * 100 if total_posts > 0 else 0
    
    bio_sobre_nicho = False
    if nicho_principal and nicho_principal in nichos:
        bio_lower = bio.lower()
        for palavra in nichos[nicho_principal]['palavras']:
            if palavra.lower() in bio_lower:
                bio_sobre_nicho = True
                break
    
    # Análise de diferenciação
    palavras_genericas = {
        'contabilidade': ['contabilidade', 'contador', 'imposto', 'declaração', 'irpf', 'empresa', 'fiscal', 'tributário'],
        'guitarra': ['guitarra', 'violão', 'música', 'solo', 'acorde'],
        'canto': ['voz', 'cantar', 'canto', 'música'],
        'marketing': ['marketing', 'vendas', 'tráfego', 'conversão'],
        'empreendedorismo': ['empreendedorismo', 'empreender', 'negócio', 'startup'],
        'saude': ['saúde', 'bem-estar', 'nutrição', 'exercício']
    }
    
    palavras_especificas = {
        'contabilidade': ['reforma tributária', 'mei', 'simples nacional', 'lucro presumido', 'lucro real', 'funrural', 'agronegócio', 'cloud', 'automação'],
        'guitarra': ['slide', 'fingerstyle', 'tapping', 'blues', 'jazz', 'bottleneck'],
        'canto': ['falsete', 'registro', 'coral', 'performance'],
        'marketing': ['tráfego pago', 'facebook ads', 'instagram ads', 'google ads', 'copywriting', 'funil de vendas'],
        'empreendedorismo': ['venture capital', 'aceleração', 'kpi', 'indicadores', 'gestão de processos'],
        'saude': ['mindfulness', 'terapia', 'ansiedade', 'estresse', 'meditação', 'hipertrofia', 'emagrecimento']
    }
    
    densidade_generica = 0
    densidade_especifica = 0
    
    if nicho_principal and nicho_principal in palavras_genericas:
        for palavra in palavras_genericas.get(nicho_principal, []):
            densidade_generica += todos_textos.count(palavra.lower())
    
    if nicho_principal and nicho_principal in palavras_especificas:
        for palavra in palavras_especificas.get(nicho_principal, []):
            densidade_especifica += todos_textos.count(palavra.lower())
    
    total_palavras_chave = densidade_generica + densidade_especifica
    if total_palavras_chave > 0:
        proporcao_especifica = densidade_especifica / total_palavras_chave
    else:
        proporcao_especifica = 0
    
    nota_diferenciacao = proporcao_especifica * 10
    nota_diferenciacao = min(10, round(nota_diferenciacao, 1))
    
    nota_bio = 10 if bio_sobre_nicho else 5
    nota_coerencia = min(10, coerencia / 10)
    nota_especificidade = especificidade * 3
    nota_especificidade = min(10, nota_especificidade)
    
    palavras_unicas = len(set(todos_textos.split()))
    nota_clareza = min(10, palavras_unicas / 20)
    
    nota_final = (nota_bio * 0.15) + (nota_coerencia * 0.25) + (nota_especificidade * 0.25) + (nota_clareza * 0.15) + (nota_diferenciacao * 0.20)
    nota_final = round(min(10, nota_final), 1)
    
    if nota_diferenciacao >= 7:
        dif_status = "ALTA diferenciação — conteúdo específico e único"
    elif nota_diferenciacao >= 4:
        dif_status = "MÉDIA diferenciação — conteúdo fala sobre o nicho, mas com pouco aprofundamento"
    else:
        dif_status = "BAIXA diferenciação — conteúdo genérico, igual ao que todo mundo fala"
    
    if nota_final >= 8:
        justificativa = f"Posicionamento MUITO CLARO e ESPECÍFICO. Nicho: {nicho_principal}. {coerencia:.0f}% dos posts sobre o nicho. {dif_status}."
    elif nota_final >= 6:
        justificativa = f"Posicionamento CLARO, mas pode ser mais específico. Nicho: {nicho_principal}. {coerencia:.0f}% dos posts sobre o nicho. {dif_status}."
    elif nota_final >= 4:
        justificativa = f"Posicionamento INDEFINIDO. Nicho: {nicho_principal}. Apenas {coerencia:.0f}% dos posts sobre o nicho. {dif_status}."
    else:
        justificativa = f"Posicionamento INEXISTENTE. Nicho não identificado."
    
    if subnichos_encontrados:
        justificativa += f" Subnichos: {', '.join(subnichos_encontrados)}."
    
    return {
        'nicho': nicho_principal or 'Nenhum nicho identificado',
        'coerencia': round(coerencia, 1),
        'especificidade': round(especificidade, 1),
        'subnichos': subnichos_encontrados,
        'densidade_generica': densidade_generica,
        'densidade_especifica': densidade_especifica,
        'proporcao_especifica': round(proporcao_especifica, 2),
        'nota_diferenciacao': nota_diferenciacao,
        'nota_sugerida': nota_final,
        'justificativa': justificativa,
        'temas_identificados': temas
    }


# =============================================================================
# 6. ANÁLISE DE CONSISTÊNCIA (V2)
# =============================================================================

def analisar_consistencia_v2(datas_posts: list) -> dict:
    """Analisa a consistência da marca com base nas datas dos posts."""
    
    if not datas_posts or len(datas_posts) < 3:
        return {
            'frequencia_media': 0,
            'regularidade': 'Dados insuficientes',
            'maior_gap': 0,
            'horario_predominante': 'N/A',
            'nota_sugerida': 3,
            'detalhes': 'Poucos posts para análise consistente.'
        }
    
    datas = []
    for d in datas_posts:
        if isinstance(d, str):
            try:
                datas.append(datetime.strptime(d, '%Y-%m-%d'))
            except:
                try:
                    datas.append(datetime.strptime(d, '%d/%m/%Y'))
                except:
                    datas.append(datetime.now())
        else:
            datas.append(d)
    
    datas = sorted(datas)
    
    dias_totais = (datas[-1] - datas[0]).days
    semanas = max(1, dias_totais / 7)
    frequencia_media = len(datas) / semanas
    frequencia_media = round(frequencia_media, 1)
    
    gaps = []
    for i in range(1, len(datas)):
        gap = (datas[i] - datas[i-1]).days
        gaps.append(gap)
    
    gap_medio = round(sum(gaps) / len(gaps), 1) if gaps else 0
    maior_gap = max(gaps) if gaps else 0
    desvio_padrao = round(np.std(gaps), 1) if gaps else 0
    
    if desvio_padrao <= 2:
        regularidade = "MUITO ALTA"
    elif desvio_padrao <= 4:
        regularidade = "ALTA"
    elif desvio_padrao <= 7:
        regularidade = "MÉDIA"
    elif desvio_padrao <= 14:
        regularidade = "BAIXA"
    else:
        regularidade = "MUITO BAIXA"
    
    nota = 0
    
    if frequencia_media >= 5:
        nota += 4
    elif frequencia_media >= 3:
        nota += 3
    elif frequencia_media >= 1.5:
        nota += 2
    elif frequencia_media >= 0.5:
        nota += 1
    
    if desvio_padrao <= 2:
        nota += 4
    elif desvio_padrao <= 4:
        nota += 3
    elif desvio_padrao <= 7:
        nota += 2
    elif desvio_padrao <= 14:
        nota += 1
    
    if maior_gap <= 3:
        nota += 2
    elif maior_gap <= 7:
        nota += 1.5
    elif maior_gap <= 14:
        nota += 1
    elif maior_gap <= 30:
        nota += 0.5
    
    nota = min(10, round(nota, 1))
    
    return {
        'frequencia_media': frequencia_media,
        'regularidade': regularidade,
        'desvio_padrao': desvio_padrao,
        'gap_medio': gap_medio,
        'maior_gap': maior_gap,
        'total_posts': len(datas),
        'periodo_dias': dias_totais,
        'horario_predominante': "N/A",
        'nota_sugerida': nota,
        'detalhes': f"{len(datas)} posts em {dias_totais} dias. Média de {frequencia_media} posts/semana."
    }


# =============================================================================
# 7. ANÁLISE DE AUTORIDADE (V3)
# =============================================================================

def analisar_autoridade_v3(bio: str, transcricoes: list, depoimentos_manuais: list = None) -> dict:
    """Analisa a autoridade da marca com base na bio, transcrições e depoimentos."""
    
    texto_completo = bio.lower() + ' ' + ' '.join(transcricoes).lower()
    
    padroes = {
        'depoimentos': [
            'depoimento', 'depoimentos', 'aluno', 'aluna', 'alunos', 'cliente', 'clientes',
            'case', 'cases', 'resultado', 'resultados', 'transformação', 'mudou', 'mudança',
            'aprendeu', 'conseguiu', 'evolução', 'progresso', 'realização', 'conquista',
            'recomenda', 'recomendação', 'testemunho', 'feedback', 'avaliação'
        ],
        'certificacoes': [
            'certificado', 'diploma', 'formado', 'graduação', 'pós', 'especialização', 
            'mestrado', 'doutorado', 'MBA', 'bacharel', 'licenciatura', 'certificação'
        ],
        'premios': [
            'prêmio', 'vencedor', 'destaque', 'finalista', 'reconhecido', 'melhor', 
            'top', 'nº 1', 'campeão', 'premiado', 'honra'
        ],
        'midia': [
            'matéria', 'entrevista', 'portal', 'revista', 'jornal', 'blog', 'podcast', 
            'tv', 'rádio', 'reportagem', 'publicação', 'artigo'
        ]
    }
    
    contagens = {}
    for categoria, palavras in padroes.items():
        contagem = 0
        for palavra in palavras:
            contagem += texto_completo.count(palavra)
        contagens[categoria] = contagem
    
    depoimentos_contagem_manual = 0
    if depoimentos_manuais:
        depoimentos_contagem_manual = len([d for d in depoimentos_manuais if d.strip()])
    
    total_depoimentos = contagens.get('depoimentos', 0) + depoimentos_contagem_manual
    
    numeros_encontrados = []
    padrao_numeros = r'(\d+)\s*(anos|alunos|clientes|resultados|casos|projetos|segundos|minutos|meses|semanas)'
    matches = re.findall(padrao_numeros, texto_completo)
    for match in matches:
        numeros_encontrados.append(f"{match[0]} {match[1]}")
    
    nota = 0
    
    if total_depoimentos >= 8:
        nota += 4
    elif total_depoimentos >= 5:
        nota += 3.5
    elif total_depoimentos >= 3:
        nota += 3
    elif total_depoimentos >= 2:
        nota += 2
    elif total_depoimentos >= 1:
        nota += 1
    
    if contagens.get('certificacoes', 0) >= 3:
        nota += 2
    elif contagens.get('certificacoes', 0) >= 1:
        nota += 1
    
    if contagens.get('premios', 0) >= 2:
        nota += 2
    elif contagens.get('premios', 0) >= 1:
        nota += 1
    
    if contagens.get('midia', 0) >= 3:
        nota += 2
    elif contagens.get('midia', 0) >= 1:
        nota += 1
    
    if len(numeros_encontrados) >= 3:
        nota += 1
    elif len(numeros_encontrados) >= 1:
        nota += 0.5
    
    nota = min(10, round(nota, 1))
    
    evidencias = []
    if total_depoimentos > 0:
        evidencias.append(f"{total_depoimentos} depoimentos encontrados ({depoimentos_contagem_manual} manuais)")
    if contagens.get('certificacoes', 0) > 0:
        evidencias.append(f"{contagens['certificacoes']} certificações mencionadas")
    if contagens.get('premios', 0) > 0:
        evidencias.append(f"{contagens['premios']} prêmios mencionados")
    if contagens.get('midia', 0) > 0:
        evidencias.append(f"{contagens['midia']} menções na mídia")
    if numeros_encontrados:
        evidencias.append(f"Números: {', '.join(numeros_encontrados[:3])}")
    
    if nota >= 8:
        justificativa = f"Autoridade MUITO ALTA. {', '.join(evidencias)}"
    elif nota >= 6:
        justificativa = f"Autoridade ALTA. {', '.join(evidencias)}"
    elif nota >= 4:
        justificativa = f"Autoridade MODERADA. {', '.join(evidencias) if evidencias else 'Poucas evidências encontradas'}"
    else:
        justificativa = "Autoridade BAIXA. Nenhuma evidência significativa encontrada."
    
    return {
        'depoimentos': total_depoimentos,
        'depoimentos_manuais': depoimentos_contagem_manual,
        'certificacoes': contagens.get('certificacoes', 0),
        'premios': contagens.get('premios', 0),
        'midia': contagens.get('midia', 0),
        'numeros': numeros_encontrados,
        'nota_sugerida': nota,
        'justificativa': justificativa,
        'evidencias': evidencias
    }


# =============================================================================
# 8. ANÁLISE DE ENGAJAMENTO (V4)
# =============================================================================

def analisar_engajamento_v4(comentarios: list) -> dict:
    """Analisa a qualidade do engajamento com base nos comentários."""
    
    if not comentarios:
        return {
            'total_comentarios': 0,
            'percentual_longo': 0,
            'percentual_perguntas': 0,
            'proporcao_texto': 0,
            'qualidade': 'BAIXO',
            'nota_sugerida': 1,
            'detalhes': 'Nenhum comentário disponível para análise.'
        }
    
    total = len(comentarios)
    
    comentarios_longos = 0
    comentarios_pergunta = 0
    total_palavras = 0
    
    for comentario in comentarios:
        texto = comentario.lower()
        palavras = len(texto.split())
        total_palavras += palavras
        
        if palavras > 10:
            comentarios_longos += 1
        
        if '?' in texto or 'como' in texto or 'qual' in texto or 'quem' in texto or 'onde' in texto:
            comentarios_pergunta += 1
    
    percentual_longo = (comentarios_longos / total) * 100 if total > 0 else 0
    percentual_perguntas = (comentarios_pergunta / total) * 100 if total > 0 else 0
    proporcao_texto = (total_palavras / max(1, total))
    
    nota = 0
    
    if total >= 20:
        nota += 3
    elif total >= 10:
        nota += 2
    elif total >= 3:
        nota += 1
    
    if percentual_longo >= 40:
        nota += 3
    elif percentual_longo >= 20:
        nota += 2
    elif percentual_longo >= 10:
        nota += 1
    
    if percentual_perguntas >= 30:
        nota += 2
    elif percentual_perguntas >= 15:
        nota += 1
    
    if proporcao_texto >= 15:
        nota += 2
    elif proporcao_texto >= 8:
        nota += 1
    
    nota = min(10, round(nota, 1))
    
    if nota >= 8:
        qualidade = "MUITO ALTO"
    elif nota >= 6:
        qualidade = "ALTO"
    elif nota >= 4:
        qualidade = "MODERADO"
    else:
        qualidade = "BAIXO"
    
    return {
        'total_comentarios': total,
        'percentual_longo': round(percentual_longo, 1),
        'percentual_perguntas': round(percentual_perguntas, 1),
        'proporcao_texto': round(proporcao_texto, 1),
        'qualidade': qualidade,
        'nota_sugerida': nota,
        'detalhes': f"{total} comentários analisados. {comentarios_longos} longos, {comentarios_pergunta} com perguntas."
    }


# =============================================================================
# 9. ANÁLISE DE PREÇO-PERCEPÇÃO (V5)
# =============================================================================

def analisar_preco_v5(preco: float, preco_mercado: Optional[float] = None, justificativa: str = "") -> dict:
    """Analisa a coerência do preço com base no benchmark de mercado."""
    
    nota = 0
    posicionamento = "Não definido"
    percentual_diferenca = 0
    
    if preco <= 0:
        return {
            'preco': preco,
            'preco_mercado': preco_mercado,
            'posicionamento': 'Não definido',
            'percentual_diferenca': 0,
            'justificativa_encontrada': bool(justificativa.strip()),
            'nota_sugerida': 3,
            'detalhes': 'Preço não informado.'
        }
    
    if preco_mercado and preco_mercado > 0:
        percentual_diferenca = ((preco - preco_mercado) / preco_mercado) * 100
        if percentual_diferenca > 30:
            posicionamento = "Premium (+{:.0f}%)".format(percentual_diferenca)
        elif percentual_diferenca > 10:
            posicionamento = "Acima da média (+{:.0f}%)".format(percentual_diferenca)
        elif percentual_diferenca > -10:
            posicionamento = "Na média ({:.0f}%)".format(percentual_diferenca)
        elif percentual_diferenca > -30:
            posicionamento = "Abaixo da média ({:.0f}%)".format(percentual_diferenca)
        else:
            posicionamento = "Entrada ({:.0f}%)".format(percentual_diferenca)
    else:
        posicionamento = "Sem benchmark"
    
    if preco_mercado and preco_mercado > 0:
        if abs(percentual_diferenca) <= 10:
            nota += 4
        elif abs(percentual_diferenca) <= 30:
            nota += 3
        elif abs(percentual_diferenca) <= 50:
            nota += 2
        else:
            nota += 1
    else:
        nota += 2
    
    if justificativa:
        palavras_chave = ['exclusivo', 'método', 'resultado', 'comprovado', 'único', 'especial', 'premium', 'garantia']
        contagem = 0
        for palavra in palavras_chave:
            if palavra.lower() in justificativa.lower():
                contagem += 1
        
        if contagem >= 4:
            nota += 4
        elif contagem >= 2:
            nota += 2
        elif contagem >= 1:
            nota += 1
    else:
        nota += 0.5
    
    if posicionamento.startswith("Premium"):
        nota += 2
    elif posicionamento.startswith("Acima"):
        nota += 1.5
    elif posicionamento.startswith("Na média"):
        nota += 1
    
    nota = min(10, round(nota, 1))
    
    return {
        'preco': preco,
        'preco_mercado': preco_mercado,
        'posicionamento': posicionamento,
        'percentual_diferenca': round(percentual_diferenca, 1),
        'justificativa_encontrada': bool(justificativa.strip()),
        'nota_sugerida': nota,
        'detalhes': f"Preço: R${preco:.2f} | Mercado: R${preco_mercado:.2f}" if preco_mercado else f"Preço: R${preco:.2f}"
    }


# =============================================================================
# 10. GOOGLE TRENDS
# =============================================================================

from pytrends.request import TrendReq
import time
from collections import Counter

def extrair_palavras_chave(transcricoes: list, top_n: int = 20) -> list:
    """Extrai as palavras mais frequentes das transcrições."""
    
    texto = ' '.join(transcricoes).lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    
    stopwords = {'a', 'o', 'e', 'é', 'que', 'de', 'da', 'do', 'para', 'com', 'um', 'uma', 
                 'os', 'as', 'na', 'no', 'em', 'por', 'seu', 'sua', 'meu', 'minha', 'isso',
                 'esse', 'essa', 'aquele', 'aquela', 'mas', 'mais', 'muito', 'pouco', 'quando',
                 'como', 'porque', 'então', 'assim', 'vou', 'fui', 'estar', 'está', 'estou',
                 'ter', 'tem', 'tive', 'ser', 'sou', 'foi', 'foram', 'vai', 'ir', 'ia'}
    
    palavras = [palavra for palavra in texto.split() if palavra not in stopwords and len(palavra) > 2]
    contagem = Counter(palavras)
    
    return contagem.most_common(top_n)


def analisar_trends(palavras_chave: list, regiao: str = 'BR', periodo: str = 'today 12-m') -> dict:
    """Analisa tendências de busca no Google Trends."""
    
    try:
        pytrends = TrendReq(hl='pt-BR', tz=-180)
        palavras = palavras_chave[:5]
        
        pytrends.build_payload(palavras, cat=0, timeframe=periodo, geo=regiao)
        
        dados_tempo = pytrends.interest_over_time()
        
        termos_relacionados = {}
        try:
            relacionados = pytrends.related_queries()
            for palavra in palavras:
                if palavra in relacionados and relacionados[palavra] is not None:
                    dados_palavra = relacionados[palavra]
                    termos_relacionados[palavra] = {
                        'rising': dados_palavra['rising'].head(5).to_dict('records') if 'rising' in dados_palavra and dados_palavra['rising'] is not None else [],
                        'top': dados_palavra['top'].head(5).to_dict('records') if 'top' in dados_palavra and dados_palavra['top'] is not None else []
                    }
                else:
                    termos_relacionados[palavra] = {'rising': [], 'top': []}
        except:
            for palavra in palavras:
                termos_relacionados[palavra] = {'rising': [], 'top': []}
        
        medias = {}
        for palavra in palavras:
            if palavra in dados_tempo.columns:
                dados_limpos = dados_tempo[palavra].dropna()
                if len(dados_limpos) > 0:
                    medias[palavra] = {
                        'media': round(dados_limpos.mean(), 2),
                        'maximo': round(dados_limpos.max(), 2),
                        'minimo': round(dados_limpos.min(), 2),
                        'tendencia': 'crescendo' if dados_limpos.iloc[-1] > dados_limpos.iloc[0] else 'diminuindo'
                    }
        
        return {
            'sucesso': True,
            'dados_tempo': dados_tempo,
            'termos_relacionados': termos_relacionados,
            'medias': medias,
            'mensagem': None
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'mensagem': f'Erro ao consultar Google Trends: {str(e)}'
        }


# =============================================================================
# 11. GRÁFICOS PARA O RELATÓRIO
# =============================================================================

def gerar_grafico_radar(notas):
    """Gera um gráfico de radar para o relatório Word."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        categorias = ['V1\nPosicionamento', 'V2\nConsistência', 'V3\nAutoridade',
                      'V4\nEngajamento', 'V5\nPreço', 'V6\nOnipresença', 'V7\nVisual']
        valores = [notas.get('v1', 0), notas.get('v2', 0), notas.get('v3', 0), 
                   notas.get('v4', 0), notas.get('v5', 0), notas.get('v6', 0), notas.get('v7', 0)]
        
        N = len(categorias)
        angulos = [n / float(N) * 2 * np.pi for n in range(N)]
        angulos += angulos[:1]
        valores_plot = valores + valores[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angulos, valores_plot, 'o-', linewidth=2, color='#2563eb', label='Perfil')
        ax.fill(angulos, valores_plot, alpha=0.25, color='#2563eb')
        ax.plot(angulos, [10] * (N + 1), '--', linewidth=1, color='#9ca3af', label='Referência (10)')
        
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, size=9)
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], size=8, color='gray')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title('Radar do Perfil da Marca', size=14, fontweight='bold', pad=20)
        
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return buffer
    except Exception as e:
        return None


def gerar_grafico_barras(notas):
    """Gera um gráfico de barras para o relatório Word."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        categorias = ['V1\nPosic.', 'V2\nConsist.', 'V3\nAutor.', 'V4\nEngaj.', 'V5\nPreço', 'V6\nOnipr.', 'V7\nVisual']
        valores = [notas.get('v1', 0), notas.get('v2', 0), notas.get('v3', 0), 
                   notas.get('v4', 0), notas.get('v5', 0), notas.get('v6', 0), notas.get('v7', 0)]
        
        cores = ['#ef4444' if v < 5 else '#f59e0b' if v < 7 else '#10b981' for v in valores]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        barras = ax.bar(categorias, valores, color=cores, edgecolor='white', linewidth=1.5)
        
        for barra, valor in zip(barras, valores):
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width() / 2., altura + 0.2,
                    f'{valor}', ha='center', va='bottom', fontweight='bold', size=11)
        
        ax.set_ylim(0, 11)
        ax.set_ylabel('Nota (0-10)', size=11)
        ax.set_title('Comparativo por Variável', size=14, fontweight='bold', pad=15)
        ax.yaxis.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return buffer
    except Exception as e:
        return None


def gerar_grafico_regua(score):
    """Gera uma régua visual de classificação para o relatório Word."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(12, 2.5))
        
        faixas = [
            (0, 4.9, '#ef4444', 'Risco'),
            (5.0, 6.4, '#f59e0b', 'Intermediaria'),
            (6.5, 7.9, '#10b981', 'Forte'),
            (8.0, 10.0, '#8b5cf6', 'Premium')
        ]
        
        for inicio, fim, cor, label in faixas:
            ax.barh(0, fim - inicio, left=inicio, height=0.4, color=cor, edgecolor='white', linewidth=2)
        
        ax.plot(score, 0, 'v', markersize=20, color='#1f2937', zorder=5)
        ax.text(score, 0.35, f'{score:.1f}', ha='center', va='bottom', 
                fontweight='bold', size=14, color='#1f2937',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#1f2937'))
        
        for inicio, fim, cor, label in faixas:
            centro = (inicio + fim) / 2
            ax.text(centro, -0.35, label, ha='center', va='top', fontsize=10, color=cor, fontweight='bold')
            ax.text(centro, -0.55, f'{inicio:.1f} - {fim:.1f}', ha='center', va='top', fontsize=8, color='gray')
        
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.8, 0.6)
        ax.axis('off')
        ax.set_title('Régua de Classificação', size=14, fontweight='bold', pad=15)
        plt.tight_layout()
        
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return buffer
    except Exception as e:
        return None


# =============================================================================
# 12. TEORIA POR VARIÁVEL
# =============================================================================

def obter_teoria_variavel(codigo):
    """Retorna a explicação teórica para cada variável."""
    
    teorias = {
        'V1': {
            'titulo': 'V1 — Posicionamento',
            'teoria': (
                'Keller (CBBE): "Salience" — a marca precisa ser facilmente lembrada e identificada em sua categoria. '
                'Aaker (Brand Equity): "Associações de Marca" — o que vem à mente quando alguém pensa na marca. '
                'Kapferer (Prisma): "Físico" — o território que a marca ocupa de forma única. '
                'Sem posicionamento claro, a marca se perde na multidão.'
            ),
            'dica': 'Escolha um nicho específico e seja O ESPECIALISTA nele.'
        },
        'V2': {
            'titulo': 'V2 — Consistência',
            'teoria': (
                'Aaker (Brand Equity): "Lealdade à Marca" — a consistência gera confiança e previsibilidade. '
                'Keller (CBBE): "Performance" — a marca entrega o que promete de forma confiável. '
                'Kapferer (Prisma): "Físico" — a expressão da marca deve ser estável ao longo do tempo.'
            ),
            'dica': 'Mantenha um calendário editorial fixo (ex: 3x por semana).'
        },
        'V3': {
            'titulo': 'V3 — Autoridade',
            'teoria': (
                'Aaker (Brand Equity): "Qualidade Percebida" — a marca é vista como competente e confiável. '
                'Keller (CBBE): "Judgment" — o consumidor acredita que a marca tem credibilidade e expertise. '
                'Kapferer (Prisma): "Físico" — as provas (depoimentos, certificados, prêmios) são evidências físicas da competência.'
            ),
            'dica': 'Colete depoimentos, documente resultados e busque validação externa.'
        },
        'V4': {
            'titulo': 'V4 — Engajamento',
            'teoria': (
                'Aaker (Brand Equity): "Lealdade à Marca" — engajamento profundo é sinal de lealdade. '
                'Keller (CBBE): "Resonance" — o estágio mais alto do CBBE, onde o consumidor se identifica com a marca. '
                'Kapferer (Prisma): "Relacionamento" — como a marca interage e se conecta com seu público.'
            ),
            'dica': 'Faça perguntas abertas e responda todos os comentários.'
        },
        'V5': {
            'titulo': 'V5 — Preço-Percepção',
            'teoria': (
                'Aaker (Brand Equity): "Qualidade Percebida" — preço premium só é aceito se a qualidade percebida for alta. '
                'Keller (CBBE): "Performance" e "Judgment" — o consumidor avalia se o preço é justo pelo que recebe. '
                'Kapferer (Prisma): "Físico" — o preço é um elemento físico da identidade da marca.'
            ),
            'dica': 'Comunique o valor antes do preço. Justifique o investimento.'
        },
        'V6': {
            'titulo': 'V6 — Onipresença',
            'teoria': (
                'Aaker (Brand Equity): "Reconhecimento de Marca" — estar presente em vários canais aumenta o reconhecimento. '
                'Keller (CBBE): "Salience" — a marca é facilmente encontrada em diferentes contextos. '
                'Ehrenberg-Bass: "Disponibilidade Física" — quanto mais fácil de encontrar, mais chances de ser escolhida.'
            ),
            'dica': 'Expanda para pelo menos 3 canais ativos (IG, YouTube, TikTok).'
        },
        'V7': {
            'titulo': 'V7 — Coerência Visual',
            'teoria': (
                'Aaker (Brand Equity): "Associações de Marca" — a estética consistente cria associações visuais fortes. '
                'Keller (CBBE): "Imagery" — as percepções visuais que o consumidor tem da marca. '
                'Kapferer (Prisma): "Físico" — a identidade visual é a manifestação mais palpável da marca.'
            ),
            'dica': 'Defina paleta de cores, cenário fixo e logo consistente.'
        }
    }
    
    return teorias.get(codigo, None)


# =============================================================================
# 13. RECOMENDAÇÕES DE PALAVRAS-CHAVE
# =============================================================================

def gerar_recomendacoes_palavras_chave(resultados_trends):
    """Gera recomendações de palavras-chave baseadas nos dados do Google Trends."""
    
    recomendacoes = {
        'palavras_em_alta': [],
        'palavras_em_queda': [],
        'termos_relacionados': [],
        'sugestoes_conteudo': []
    }
    
    if not resultados_trends or not resultados_trends.get('sucesso'):
        return recomendacoes
    
    medias = resultados_trends.get('medias', {})
    for palavra, dados in medias.items():
        if dados.get('tendencia') == 'crescendo':
            recomendacoes['palavras_em_alta'].append({
                'palavra': palavra,
                'media': dados.get('media', 0),
                'tendencia': 'crescendo'
            })
        else:
            recomendacoes['palavras_em_queda'].append({
                'palavra': palavra,
                'media': dados.get('media', 0),
                'tendencia': 'diminuindo'
            })
    
    termos = resultados_trends.get('termos_relacionados', {})
    for palavra, dados in termos.items():
        if dados.get('rising'):
            for item in dados['rising'][:3]:
                recomendacoes['termos_relacionados'].append({
                    'termo': item['query'],
                    'crescimento': item.get('value', 'N/A'),
                    'baseado_em': palavra
                })
    
    for palavra in recomendacoes['palavras_em_alta']:
        recomendacoes['sugestoes_conteudo'].append(
            f"Crie conteúdo sobre '{palavra['palavra']}' — está em alta no Google Trends"
        )
    
    for termo in recomendacoes['termos_relacionados'][:5]:
        recomendacoes['sugestoes_conteudo'].append(
            f"Explore o termo '{termo['termo']}' — está crescendo (+{termo['crescimento']})"
        )
    
    return recomendacoes
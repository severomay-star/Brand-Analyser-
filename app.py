"""
===============================================================================
BRANDING ANALYZER — Interface Streamlit
Versão Completa com Laudo Profissional Bonito
===============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from io import BytesIO
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from branding_analyzer import (
    calcular_score_ponderado,
    classificar_marca,
    gerar_recomendacoes,
    dicas_arquétipo,
    analisar_posicionamento_v1,
    extrair_palavras_chave,
    analisar_trends,
    analisar_consistencia_v2,
    analisar_autoridade_v3,
    analisar_engajamento_v4,
    analisar_preco_v5,
    gerar_grafico_radar,
    gerar_grafico_barras,
    gerar_grafico_regua,
    obter_teoria_variavel,
    gerar_recomendacoes_palavras_chave
)

st.set_page_config(
    page_title="Branding Analyzer",
    page_icon="🎯",
    layout="wide"
)


# ============================================================================
# FUNÇÕES PARA LER ARQUIVOS TXT
# ============================================================================

def ler_arquivo_txt(arquivo):
    """Lê o conteúdo de um arquivo .txt e retorna como string."""
    try:
        conteudo = arquivo.read().decode('utf-8')
        return conteudo
    except UnicodeDecodeError:
        try:
            arquivo.seek(0)
            conteudo = arquivo.read().decode('latin-1')
            return conteudo
        except:
            try:
                arquivo.seek(0)
                conteudo = arquivo.read().decode('windows-1252')
                return conteudo
            except:
                return None
    except Exception:
        return None


def extrair_linhas_arquivo(arquivo):
    """Lê um arquivo .txt e retorna uma lista de linhas não vazias."""
    conteudo = ler_arquivo_txt(arquivo)
    
    if not conteudo:
        return []
    
    conteudo = conteudo.replace('\r\n', '\n').replace('\r', '\n')
    
    linhas = []
    for linha in conteudo.split('\n'):
        linha_limpa = linha.strip()
        if linha_limpa and len(linha_limpa) >= 2:
            linhas.append(linha_limpa)
    
    return linhas


def extrair_linhas_multiplos_arquivos(arquivos):
    """Lê MÚLTIPLOS arquivos .txt e retorna uma lista única de linhas."""
    if not arquivos:
        return []
    
    todas_linhas = []
    for arquivo in arquivos:
        linhas = extrair_linhas_arquivo(arquivo)
        todas_linhas.extend(linhas)
    
    return todas_linhas


# ============================================================================
# ALERTAS DE DIFERENCIAÇÃO
# ============================================================================

def alerta_diferenciacao(nota_diff):
    """Retorna o HTML do alerta de diferenciação."""
    
    if nota_diff >= 7:
        return """
        <div style="background: #d1fae5; border-left: 4px solid #10b981; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <strong style="color: #065f46;">✅ ALTA DIFERENCIAÇÃO</strong><br>
            <span style="color: #065f46;">Seu conteúdo é específico e único. Você está no caminho certo para se tornar uma referência!</span>
            <br><br>
            <span style="color: #065f46; font-size: 0.9rem;">💡 Continue aprofundando os temas e mostrando sua autoridade no assunto.</span>
        </div>
        """
    elif nota_diff >= 4:
        return """
        <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <strong style="color: #92400e;">⚠️ MÉDIA DIFERENCIAÇÃO</strong><br>
            <span style="color: #92400e;">Você fala sobre o nicho, mas os temas são genéricos — exatamente o que todo mundo está falando.</span>
            <br><br>
            <span style="color: #92400e; font-size: 0.9rem;">💡 Considere definir um sub-nicho mais específico.</span>
        </div>
        """
    else:
        return """
        <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <strong style="color: #991b1b;">🔴 BAIXA DIFERENCIAÇÃO</strong><br>
            <span style="color: #991b1b;">Seu conteúdo é genérico e não se destaca.</span>
            <br><br>
            <span style="color: #991b1b; font-size: 0.9rem;">💡 Defina um público muito específico e um problema claro.</span>
        </div>
        """


# ============================================================================
# GRÁFICO DO GOOGLE TRENDS
# ============================================================================

def criar_grafico_trends(dados_tempo):
    """Cria gráfico de linha para dados do Google Trends."""
    fig = go.Figure()
    for coluna in dados_tempo.columns:
        fig.add_trace(go.Scatter(
            x=dados_tempo.index,
            y=dados_tempo[coluna],
            mode='lines',
            name=coluna,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title='Interesse ao longo do tempo',
        xaxis_title='Data',
        yaxis_title='Interesse relativo',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig


# ============================================================================
# FUNÇÃO PARA GERAR DOCX PROFISSIONAL
# ============================================================================

def gerar_docx(dados):
    """
    Gera um documento Word PROFISSIONAL com:
    - Capa executiva
    - Cabeçalhos e seções coloridas
    - Gráficos grandes e centralizados
    - Tabelas com cores
    - Caixas de alerta coloridas
    - Rodapé profissional
    """
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    
    doc = docx.Document()
    
    # ========================================================================
    # CONFIGURAÇÃO DE ESTILOS
    # ========================================================================
    
    COR_PRIMARIA = RGBColor(0x1F, 0x29, 0x37)
    COR_SECUNDARIA = RGBColor(0x25, 0x63, 0xEB)
    COR_SUCESSO = RGBColor(0x10, 0xB9, 0x81)
    COR_ALERTA = RGBColor(0xF5, 0x9E, 0x0B)
    COR_ERRO = RGBColor(0xEF, 0x44, 0x44)
    COR_CINZA = RGBColor(0x6B, 0x72, 0x80)
    COR_BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
    
    # Margens da página
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
    
    # ========================================================================
    # FUNÇÕES AUXILIARES
    # ========================================================================
    
    def adicionar_titulo_secao(doc, numero, texto):
        """Adiciona um título de seção com cor e numeração."""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        
        run_num = p.add_run(f'{numero}. ')
        run_num.bold = True
        run_num.font.size = Pt(16)
        run_num.font.color.rgb = COR_SECUNDARIA
        
        run_texto = p.add_run(texto)
        run_texto.bold = True
        run_texto.font.size = Pt(16)
        run_texto.font.color.rgb = COR_PRIMARIA
        
        return p
    
    def adicionar_subtitulo(doc, texto):
        """Adiciona um subtítulo."""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(texto)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = COR_PRIMARIA
        return p
    
    def adicionar_tabela_estilizada(doc, cabecalhos, dados, cores_notas=None):
        """Adiciona uma tabela estilizada com cabeçalho colorido."""
        table = doc.add_table(rows=1, cols=len(cabecalhos))
        table.style = 'Light Grid Accent 1'
        
        hdr = table.rows[0].cells
        for i, cabecalho in enumerate(cabecalhos):
            hdr[i].text = ''
            p = hdr[i].paragraphs[0]
            run = p.add_run(cabecalho)
            run.bold = True
            run.font.color.rgb = COR_BRANCO
            run.font.size = Pt(10)
            
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), '1F2937')
            hdr[i]._tc.get_or_add_tcPr().append(shading)
        
        for linha_dados in dados:
            row = table.add_row().cells
            for i, valor in enumerate(linha_dados):
                row[i].text = ''
                p = row[i].paragraphs[0]
                run = p.add_run(str(valor))
                run.font.size = Pt(10)
                
                if cores_notas and i in cores_notas:
                    try:
                        nota = float(valor)
                        if nota >= 7:
                            run.font.color.rgb = COR_SUCESSO
                            run.bold = True
                        elif nota >= 5:
                            run.font.color.rgb = COR_ALERTA
                            run.bold = True
                        else:
                            run.font.color.rgb = COR_ERRO
                            run.bold = True
                    except:
                        pass
        
        return table
    
    # ========================================================================
    # CAPA
    # ========================================================================
    
    for _ in range(3):
        doc.add_paragraph()
    
    titulo = doc.add_paragraph()
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_titulo = titulo.add_run('BRANDING ANALYZER')
    run_titulo.font.size = Pt(36)
    run_titulo.bold = True
    run_titulo.font.color.rgb = COR_PRIMARIA
    
    subtitulo = doc.add_paragraph()
    subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = subtitulo.add_run('Análise Científica de Branding')
    run_sub.font.size = Pt(18)
    run_sub.font.color.rgb = COR_SECUNDARIA
    run_sub.italic = True
    
    doc.add_paragraph()
    
    linha = doc.add_paragraph()
    linha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_linha = linha.add_run('━' * 30)
    run_linha.font.color.rgb = COR_SECUNDARIA
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    marca = dados.get('marca', {})
    nome_marca = marca.get('nome', 'Marca não informada')
    
    nome_par = doc.add_paragraph()
    nome_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_nome = nome_par.add_run(nome_marca)
    run_nome.font.size = Pt(28)
    run_nome.bold = True
    run_nome.font.color.rgb = COR_SECUNDARIA
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    score = dados.get('score', {})
    score_valor = score.get('score_ponderado', 0)
    classificacao = score.get('classificacao', 'N/A')
    
    score_par = doc.add_paragraph()
    score_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_score = score_par.add_run(f'Score: {score_valor}/10')
    run_score.font.size = Pt(22)
    run_score.bold = True
    run_score.font.color.rgb = COR_PRIMARIA
    
    class_par = doc.add_paragraph()
    class_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_class = class_par.add_run(classificacao.upper())
    run_class.font.size = Pt(16)
    run_class.bold = True
    
    if score_valor >= 6.5:
        run_class.font.color.rgb = COR_SUCESSO
    elif score_valor >= 5:
        run_class.font.color.rgb = COR_ALERTA
    else:
        run_class.font.color.rgb = COR_ERRO
    
    for _ in range(5):
        doc.add_paragraph()
    
    data_par = doc.add_paragraph()
    data_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_data = data_par.add_run(f'Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}')
    run_data.font.size = Pt(11)
    run_data.font.color.rgb = COR_CINZA
    
    rodape_capa = doc.add_paragraph()
    rodape_capa.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_rod = rodape_capa.add_run('Baseado em Aaker, Keller, Kapferer e Ehrenberg-Bass')
    run_rod.font.size = Pt(10)
    run_rod.italic = True
    run_rod.font.color.rgb = COR_CINZA
    
    # ========================================================================
    # QUEBRA DE PÁGINA
    # ========================================================================
    doc.add_page_break()
    
    # ========================================================================
    # 1. DADOS DA MARCA
    # ========================================================================
    adicionar_titulo_secao(doc, 1, 'Dados da Marca')
    
    doc.add_paragraph(f'Nome: {marca.get("nome", "Não informado")}')
    doc.add_paragraph(f'Segmento: {marca.get("segmento", "Não informado")}')
    doc.add_paragraph(f'Seguidores: {marca.get("seguidores", 0):,}')
    doc.add_paragraph(f'Crescimento mensal: {marca.get("crescimento", 0)}%/mês')
    doc.add_paragraph(f'Produtos ativos: {marca.get("produtos", 0)}')
    doc.add_paragraph(f'Canais ativos: {marca.get("canais", 0)}')
    doc.add_paragraph(f'Autoridade externa: {"Sim" if marca.get("autoridade") else "Não"}')
    doc.add_paragraph(f'Arquétipo: {marca.get("arquétipo", "Não definido")}')
    
    doc.add_paragraph()
    
    # ========================================================================
    # 2. SCORE E RÉGUA
    # ========================================================================
    adicionar_titulo_secao(doc, 2, 'Score Total')
    
    doc.add_paragraph(f'Score Simples: {score.get("score_simples", "N/A")}/10')
    doc.add_paragraph(f'Score Ponderado: {score.get("score_ponderado", "N/A")}/10')
    doc.add_paragraph(f'Classificação: {score.get("classificacao", "N/A")}')
    
    try:
        img_regua = gerar_grafico_regua(score_valor)
        if img_regua:
            doc.add_picture(img_regua, width=Inches(6.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except:
        pass
    
    doc.add_paragraph()
    
    # ========================================================================
    # 3. VISUALIZAÇÃO (GRÁFICOS)
    # ========================================================================
    adicionar_titulo_secao(doc, 3, 'Visualização do Perfil')
    
    notas = dados.get('notas', {})
    
    adicionar_subtitulo(doc, 'Radar do Perfil')
    try:
        img_radar = gerar_grafico_radar(notas)
        if img_radar:
            doc.add_picture(img_radar, width=Inches(5.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except:
        pass
    
    doc.add_paragraph()
    adicionar_subtitulo(doc, 'Comparativo por Variável')
    try:
        img_barras = gerar_grafico_barras(notas)
        if img_barras:
            doc.add_picture(img_barras, width=Inches(6.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except:
        pass
    
    doc.add_paragraph()
    
    # ========================================================================
    # 4. BREAKDOWN
    # ========================================================================
    adicionar_titulo_secao(doc, 4, 'Detalhamento por Variável')
    
    cabecalhos = ['Variável', 'Código', 'Nota', 'Peso', 'Contribuição', '% do Score']
    dados_tabela = []
    for var, info in score.get('breakdown', {}).items():
        dados_tabela.append([
            var,
            info.get('codigo', ''),
            str(info.get('nota', 0)),
            str(info.get('peso', 0)),
            str(info.get('contribuicao', 0)),
            f"{info.get('percentual', 0):.1f}%"
        ])
    
    adicionar_tabela_estilizada(doc, cabecalhos, dados_tabela, cores_notas={2})
    
    doc.add_paragraph()
    
    # ========================================================================
    # 5. CLASSIFICAÇÃO
    # ========================================================================
    adicionar_titulo_secao(doc, 5, 'Classificação da Marca')
    
    classificacao_dados = dados.get('classificacao', {})
    doc.add_paragraph(f'Status: {classificacao_dados.get("classificacao", "N/A")}')
    doc.add_paragraph(f'Nível: {classificacao_dados.get("nivel", "N/A")}')
    doc.add_paragraph(f'Ação Recomendada: {classificacao_dados.get("acao_recomendada", "N/A")}')
    
    if classificacao_dados.get('evidencias'):
        doc.add_paragraph()
        adicionar_subtitulo(doc, 'Evidências Encontradas')
        for e in classificacao_dados['evidencias']:
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(e)
    
    doc.add_paragraph()
    
    # ========================================================================
    # 6. RECOMENDAÇÕES COM TEORIA
    # ========================================================================
    doc.add_page_break()
    adicionar_titulo_secao(doc, 6, 'Recomendações com Fundamentação Teórica')
    
    recomendacoes = dados.get('recomendacoes', {})
    
    resumo_par = doc.add_paragraph()
    run_resumo = resumo_par.add_run(f'Resumo: {recomendacoes.get("resumo", "")}')
    run_resumo.italic = True
    run_resumo.font.size = Pt(11)
    
    doc.add_paragraph()
    
    def exibir_item_recomendacao(doc, item, cor_categoria):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        run = p.add_run(f'● {item["variavel"]} — Nota {item["nota"]}/10')
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = cor_categoria
        
        doc.add_paragraph(f'{item["recomendacao"]}', style='List Bullet')
        
        teoria = obter_teoria_variavel(item['variavel'])
        if teoria:
            p_teoria = doc.add_paragraph()
            p_teoria.paragraph_format.left_indent = Inches(0.3)
            run_t = p_teoria.add_run('📚 Fundamentação Teórica: ')
            run_t.bold = True
            run_t.italic = True
            run_t.font.size = Pt(10)
            run_t.font.color.rgb = COR_CINZA
            
            r = p_teoria.add_run(teoria['teoria'])
            r.italic = True
            r.font.size = Pt(10)
            r.font.color.rgb = COR_CINZA
            
            p_dica = doc.add_paragraph()
            p_dica.paragraph_format.left_indent = Inches(0.3)
            run_d = p_dica.add_run('💡 Dica Prática: ')
            run_d.bold = True
            run_d.font.size = Pt(10)
            run_d.font.color.rgb = COR_SECUNDARIA
            p_dica.add_run(teoria['dica']).font.size = Pt(10)
    
    if recomendacoes.get('criticas'):
        adicionar_subtitulo(doc, '🔴 Críticas (nota < 5) — Atenção Imediata')
        for item in recomendacoes['criticas']:
            exibir_item_recomendacao(doc, item, COR_ERRO)
    
    if recomendacoes.get('importantes'):
        adicionar_subtitulo(doc, '🟡 Melhorar (nota 5-7)')
        for item in recomendacoes['importantes']:
            exibir_item_recomendacao(doc, item, COR_ALERTA)
    
    if recomendacoes.get('otimizacoes'):
        adicionar_subtitulo(doc, '🟢 Otimizações (nota > 7)')
        for item in recomendacoes['otimizacoes']:
            exibir_item_recomendacao(doc, item, COR_SUCESSO)
    
    doc.add_paragraph()
    
    # ========================================================================
    # 7. ARQUÉTIPO
    # ========================================================================
    if recomendacoes.get('arquétipo'):
        doc.add_page_break()
        adicionar_titulo_secao(doc, 7, 'Arquétipo Dominante')
        
        a = recomendacoes['arquétipo']
        doc.add_paragraph(f'Atual: {a["atual"]}')
        doc.add_paragraph(f'Ação: {a["acao"]}')
        
        dicas = dicas_arquétipo(a['atual'])
        if dicas:
            adicionar_subtitulo(doc, 'Diretrizes de Posicionamento')
            doc.add_paragraph(f'🎯 Posicionamento: {dicas["posicionamento"]}')
            doc.add_paragraph(f'📝 Conteúdo: {dicas["conteudo"]}')
            doc.add_paragraph(f'💬 Linguagem: {dicas["linguagem"]}')
            doc.add_paragraph(f'🎨 Visual: {dicas["visual"]}')
            doc.add_paragraph(f'📢 CTA: {dicas["cta"]}')
        
        doc.add_paragraph()
    
    # ========================================================================
    # 8. PALAVRAS-CHAVE (GOOGLE TRENDS)
    # ========================================================================
    trends_dados = dados.get('trends', {})
    if trends_dados and trends_dados.get('sucesso'):
        adicionar_titulo_secao(doc, 8, 'Recomendações de Palavras-Chave')
        
        recomendacoes_kw = gerar_recomendacoes_palavras_chave(trends_dados)
        
        if recomendacoes_kw['palavras_em_alta']:
            adicionar_subtitulo(doc, '🔥 Palavras em Alta — Aproveite!')
            for item in recomendacoes_kw['palavras_em_alta']:
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(f'{item["palavra"]} ')
                run.bold = True
                run.font.color.rgb = COR_SUCESSO
                p.add_run(f'(média: {item["media"]})')
        
        if recomendacoes_kw['palavras_em_queda']:
            adicionar_subtitulo(doc, '📉 Palavras em Queda — Cuidado')
            for item in recomendacoes_kw['palavras_em_queda']:
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(f'{item["palavra"]} ')
                run.bold = True
                run.font.color.rgb = COR_ERRO
                p.add_run(f'(média: {item["media"]})')
        
        if recomendacoes_kw['termos_relacionados']:
            adicionar_subtitulo(doc, '🔍 Termos Relacionados em Alta')
            for item in recomendacoes_kw['termos_relacionados']:
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(f'{item["termo"]} ')
                run.bold = True
                p.add_run(f'(+{item["crescimento"]}) — relacionado a "{item["baseado_em"]}"')
        
        if recomendacoes_kw['sugestoes_conteudo']:
            adicionar_subtitulo(doc, '💡 Sugestões de Conteúdo')
            for sugestao in recomendacoes_kw['sugestoes_conteudo']:
                doc.add_paragraph(sugestao, style='List Bullet')
        
        doc.add_paragraph()
    
    # ========================================================================
    # RODAPÉ FINAL
    # ========================================================================
    doc.add_page_break()
    
    for _ in range(8):
        doc.add_paragraph()
    
    final_par = doc.add_paragraph()
    final_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_final = final_par.add_run('━' * 30)
    run_final.font.color.rgb = COR_SECUNDARIA
    
    final_par2 = doc.add_paragraph()
    final_par2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_final2 = final_par2.add_run('Branding Analyzer v1.0')
    run_final2.font.size = Pt(14)
    run_final2.bold = True
    run_final2.font.color.rgb = COR_PRIMARIA
    
    final_par3 = doc.add_paragraph()
    final_par3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_final3 = final_par3.add_run('Baseado em Aaker, Keller, Kapferer e Ehrenberg-Bass')
    run_final3.font.size = Pt(11)
    run_final3.italic = True
    run_final3.font.color.rgb = COR_CINZA
    
    final_par4 = doc.add_paragraph()
    final_par4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_final4 = final_par4.add_run(f'© {datetime.now().year} — Todos os direitos reservados')
    run_final4.font.size = Pt(10)
    run_final4.font.color.rgb = COR_CINZA
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


# ============================================================================
# MANUAL DO ANALISTA
# ============================================================================

def mostrar_manual():
    with st.expander("📘 Manual do Analista", expanded=False):
        st.markdown("""
        ### 📋 Regra de Amostragem

        | Total de posts | Blocos | Posts por bloco | Amostra |
        |---------------|--------|-----------------|---------|
        | Até 150 | 3 | 5 | 15 |
        | 151 – 500 | 4 | 5 | 20 |
        | 501 – 1.500 | 5 | 5 | 25 |
        | Acima de 1.500 | 6 | 5 | 30 |
        """)

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "V1", "V2", "V3", "V4", "V5", "V6", "V7"
        ])

        with tab1:
            st.markdown("""
            ### V1 — Posicionamento
            | Nota | Critério |
            |------|----------|
            | 0 | Sem nicho definido |
            | 3 | Nicho amplo |
            | 5 | Nicho definido, mas comum |
            | 7 | Nicho específico |
            | 10 | Território exclusivo |
            """)

        with tab2:
            st.markdown("""
            ### V2 — Consistência
            | Nota | Critério |
            |------|----------|
            | 0 | Muda constantemente |
            | 3 | Publica esporadicamente |
            | 5 | Frequência razoável, com gaps |
            | 7 | Frequência regular |
            | 10 | Cadência constante há anos |
            """)

        with tab3:
            st.markdown("""
            ### V3 — Autoridade
            | Nota | Critério |
            |------|----------|
            | 0 | Nenhuma prova |
            | 3 | Menciona, mas não prova |
            | 5 | Alguma prova social |
            | 7 | Provas consistentes |
            | 10 | Autoridade validada externamente |
            """)

        with tab4:
            st.markdown("""
            ### V4 — Engajamento
            | Nota | Critério |
            |------|----------|
            | 0 | Comentários genéricos |
            | 3 | Interação rasa |
            | 5 | Com perguntas/reflexões |
            | 7 | Comunidade ativa |
            | 10 | Audiência gera conteúdo |
            """)

        with tab5:
            st.markdown("""
            ### V5 — Preço-Percepção
            | Nota | Critério |
            |------|----------|
            | 0 | Preço incoerente |
            | 3 | Leve descompasso |
            | 5 | Aceitável, sem clareza |
            | 7 | Coerente com autoridade |
            | 10 | Preço reforça posicionamento |
            """)

        with tab6:
            st.markdown("""
            ### V6 — Onipresença
            | Nota | Critério |
            |------|----------|
            | 0 | 1 canal, baixa frequência |
            | 3 | 1 canal, frequência razoável |
            | 5 | 2 canais ativos |
            | 7 | 3+ canais ativos |
            | 10 | Multi-canal dominante |
            """)

        with tab7:
            st.markdown("""
            ### V7 — Coerência Visual
            Soma de 5 subcritérios (0-2 cada):
            - Paleta de cores
            - Vestimenta
            - Cenário
            - Qualidade técnica
            - Marca visual
            """)


# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def criar_radar(notas):
    nomes = {
        'v1': 'Posicionamento', 'v2': 'Consistência', 'v3': 'Autoridade',
        'v4': 'Engajamento', 'v5': 'Preço-Percepção', 'v6': 'Onipresença',
        'v7': 'Coerência Visual'
    }
    df = pd.DataFrame({
        'Variável': [nomes.get(k, k.upper()) for k in notas.keys()],
        'Nota': list(notas.values())
    })
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df['Nota'],
        theta=df['Variável'],
        fill='toself',
        name='Perfil',
        line_color='#2563eb',
        fillcolor='rgba(37, 99, 235, 0.2)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[10] * len(df),
        theta=df['Variável'],
        fill=None,
        name='Referência',
        line_color='#9ca3af',
        line_dash='dash'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        height=400,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig


def criar_barras(notas):
    nomes = {
        'v1': 'Posicionamento', 'v2': 'Consistência', 'v3': 'Autoridade',
        'v4': 'Engajamento', 'v5': 'Preço-Percepção', 'v6': 'Onipresença',
        'v7': 'Coerência Visual'
    }
    df = pd.DataFrame({
        'Variável': [nomes.get(k, k.upper()) for k in notas.keys()],
        'Nota': list(notas.values())
    })
    cores = ['#ef4444' if n < 5 else '#f59e0b' if n < 7 else '#10b981' for n in df['Nota']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Variável'],
        y=df['Nota'],
        marker_color=cores,
        text=df['Nota'],
        textposition='outside'
    ))
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(range=[0, 10.5])
    )
    return fig


# ============================================================================
# EXIBIÇÃO DE ANÁLISES OBJETIVAS
# ============================================================================

def exibir_analise_v2(resultado):
    if resultado and resultado.get('total_posts', 0) > 0:
        st.markdown(f"""
        **📅 Frequência média:** {resultado['frequencia_media']} posts/semana
        **📊 Regularidade:** {resultado['regularidade']} (desvio: {resultado['desvio_padrao']} dias)
        **📏 Gap médio:** {resultado['gap_medio']} dias | **Maior gap:** {resultado['maior_gap']} dias
        **📝 Total:** {resultado['total_posts']} posts em {resultado['periodo_dias']} dias
        """)
        nota = resultado['nota_sugerida']
        st.progress(nota/10)
        st.caption(f"💡 **Nota sugerida: {nota}/10** — {resultado['detalhes']}")
    else:
        st.info("📅 Insira as datas dos posts para análise de consistência.")


def exibir_analise_v3(resultado):
    if resultado:
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("📝 Depoimentos", resultado.get('depoimentos', 0))
        with col_b:
            st.metric("🎓 Certificações", resultado.get('certificacoes', 0))
        with col_c:
            st.metric("🏆 Prêmios", resultado.get('premios', 0))
        with col_d:
            st.metric("📰 Mídia", resultado.get('midia', 0))
        
        if resultado.get('depoimentos_manuais', 0) > 0:
            st.success(f"✅ {resultado['depoimentos_manuais']} depoimentos manuais adicionados!")
        
        if resultado.get('numeros'):
            st.write(f"**Números encontrados:** {', '.join(resultado['numeros'][:3])}")
        
        nota = resultado['nota_sugerida']
        st.progress(nota/10)
        st.caption(f"💡 **Nota sugerida: {nota}/10** — {resultado['justificativa']}")


def exibir_analise_v4(resultado):
    if resultado and resultado.get('total_comentarios', 0) > 0:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("💬 Comentários", resultado['total_comentarios'])
        with col_b:
            st.metric("📝 Longos", f"{resultado['percentual_longo']:.1f}%")
        with col_c:
            st.metric("❓ Perguntas", f"{resultado['percentual_perguntas']:.1f}%")
        
        st.write(f"**Qualidade:** {resultado['qualidade']} | **Média de palavras:** {resultado['proporcao_texto']}")
        
        nota = resultado['nota_sugerida']
        st.progress(nota/10)
        st.caption(f"💡 **Nota sugerida: {nota}/10** — {resultado['detalhes']}")
    else:
        st.info("💬 Insira os comentários dos posts para análise de engajamento.")


def exibir_analise_v5(resultado):
    if resultado and resultado.get('preco', 0) > 0:
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("💰 Preço", f"R$ {resultado['preco']:.2f}")
        with col_b:
            st.metric("📊 Posicionamento", resultado['posicionamento'])
        
        if resultado.get('preco_mercado'):
            st.write(f"**Mercado:** R$ {resultado['preco_mercado']:.2f} | **Diferença:** {resultado['percentual_diferenca']:.1f}%")
        
        st.write(f"**Justificativa de valor:** {'✅ Encontrada' if resultado['justificativa_encontrada'] else '❌ Não encontrada'}")
        
        nota = resultado['nota_sugerida']
        st.progress(nota/10)
        st.caption(f"💡 **Nota sugerida: {nota}/10** — {resultado['detalhes']}")
    else:
        st.info("💰 Insira o preço do produto/serviço para análise.")


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("🎯 Branding Analyzer")
    st.markdown("---")

    st.subheader("📋 Dados Básicos")
    nome_marca = st.text_input("Nome da marca/perfil", placeholder="Ex: Juliana Vieira")
    segmento = st.selectbox("Segmento", ["Música", "Contabilidade", "Outro"], index=0)
    segmento_key = "musica" if segmento == "Música" else "contabilidade" if segmento == "Contabilidade" else "outro"

    # V1
    st.markdown("---")
    with st.expander("📝 Análise de Posicionamento (V1)", expanded=False):
        st.markdown("**Como usar:** Faça upload da bio e transcrições (.txt)")
        
        st.caption("**📄 Bio do perfil**")
        bio_arquivo = st.file_uploader("Upload da bio (.txt)", type=['txt'], key="bio_upload")
        bio_input = st.text_area("Bio (cole ou edite)", placeholder="Cole a biografia aqui...", height=80, key="bio_input_manual")
        
        if bio_arquivo:
            bio_input = ler_arquivo_txt(bio_arquivo)
            if bio_input:
                st.success(f"✅ Bio carregada ({len(bio_input)} caracteres)")
        
        st.caption("**📄 Transcrições dos posts (múltiplos arquivos)**")
        transcricoes_arquivos = st.file_uploader(
            "Upload das transcrições (.txt)",
            type=['txt'],
            accept_multiple_files=True,
            key="transcricoes_upload"
        )
        transcricoes_input = st.text_area(
            "Transcrições (cole ou edite)",
            placeholder="Cole cada transcrição em uma linha separada...",
            height=100,
            key="transcricoes_input_manual"
        )
        
        if transcricoes_arquivos:
            todas_linhas = extrair_linhas_multiplos_arquivos(transcricoes_arquivos)
            if todas_linhas:
                transcricoes_input = '\n'.join(todas_linhas)
                st.success(f"✅ {len(todas_linhas)} transcrições carregadas de {len(transcricoes_arquivos)} arquivo(s)")
        
        col_btn, col_status = st.columns([1, 2])
        
        with col_btn:
            if st.button("🔍 Analisar V1", key="analisar_v1", use_container_width=True):
                if bio_input and transcricoes_input:
                    transcricoes_list = [t.strip() for t in transcricoes_input.split('\n') if t.strip()]
                    
                    with st.spinner("Analisando posicionamento..."):
                        resultado = analisar_posicionamento_v1(bio_input, transcricoes_list)
                        
                        st.session_state['v1_analise'] = resultado
                        st.session_state['v1_nota_sugerida'] = resultado['nota_sugerida']
                        st.session_state['v1_transcricoes'] = transcricoes_list
                        st.session_state['v1_bio'] = bio_input
                        
                        st.success(f"✅ Nota sugerida: {resultado['nota_sugerida']}/10")
                else:
                    st.warning("Preencha a bio e pelo menos uma transcrição.")
        
        with col_status:
            if st.session_state.get('v1_analise'):
                v1_result = st.session_state['v1_analise']
                st.info(f"📊 {v1_result['nicho']} | Coerência: {v1_result['coerencia']:.1f}%")
            else:
                st.caption("⏳ Aguardando análise...")
        
        if st.session_state.get('v1_analise'):
            st.markdown("---")
            v1_result = st.session_state['v1_analise']
            
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Nota", f"{v1_result['nota_sugerida']}/10")
            with col_r2:
                st.metric("Coerência", f"{v1_result['coerencia']:.1f}%")
            with col_r3:
                if st.button("✅ Aplicar nota", key="aplicar_v1", use_container_width=True):
                    st.session_state['v1'] = int(v1_result['nota_sugerida'])
                    st.session_state['v1_override'] = True
                    st.success("✅ V1 ajustado!")
            
            st.markdown(f"**Justificativa:** {v1_result['justificativa']}")
            
            if v1_result.get('subnichos') and len(v1_result['subnichos']) > 0:
                st.write(f"**Subnichos identificados:** {', '.join(v1_result['subnichos'])}")
                st.caption(f"**Nível de especificidade:** {v1_result['especificidade']}/3")
            
            if v1_result.get('nota_diferenciacao') is not None:
                st.markdown("---")
                st.caption("**📊 Análise de Diferenciação**")
                
                col_diff1, col_diff2, col_diff3 = st.columns(3)
                with col_diff1:
                    st.metric("Palavras Genéricas", v1_result.get('densidade_generica', 0))
                with col_diff2:
                    st.metric("Palavras Específicas", v1_result.get('densidade_especifica', 0))
                with col_diff3:
                    st.metric("Nota de Diferenciação", f"{v1_result.get('nota_diferenciacao', 0)}/10")
                
                nota_diff = v1_result.get('nota_diferenciacao', 0)
                st.markdown(alerta_diferenciacao(nota_diff), unsafe_allow_html=True)
            
            with st.expander("📋 Temas identificados"):
                for tema, qtde in sorted(v1_result['temas_identificados'].items(), key=lambda x: x[1], reverse=True):
                    st.write(f"- {tema}: {qtde} menções")

    # V2
    st.markdown("---")
    with st.expander("📅 Análise de Consistência (V2)", expanded=False):
        st.markdown("**Como usar:** Faça upload das datas dos posts (.txt)")
        
        datas_arquivos = st.file_uploader(
            "Upload das datas (.txt) — múltiplos arquivos",
            type=['txt'],
            accept_multiple_files=True,
            key="datas_upload"
        )
        datas_input = st.text_area(
            "Datas (uma por linha)",
            placeholder="2024-01-15\n2024-01-18\n2024-01-22",
            height=100,
            key="datas_input_manual"
        )
        
        if datas_arquivos:
            todas_linhas = extrair_linhas_multiplos_arquivos(datas_arquivos)
            if todas_linhas:
                datas_input = '\n'.join(todas_linhas)
                st.success(f"✅ {len(todas_linhas)} datas carregadas")
        
        col_btn2, col_status2 = st.columns([1, 2])
        
        with col_btn2:
            if st.button("📊 Analisar V2", key="analisar_v2", use_container_width=True):
                if datas_input:
                    datas_list = [d.strip() for d in datas_input.split('\n') if d.strip()]
                    
                    with st.spinner("Analisando consistência..."):
                        resultado = analisar_consistencia_v2(datas_list)
                        
                        st.session_state['v2_analise'] = resultado
                        st.session_state['v2_nota_sugerida'] = resultado['nota_sugerida']
                        
                        st.success(f"✅ Nota sugerida: {resultado['nota_sugerida']}/10")
                else:
                    st.warning("Preencha pelo menos 3 datas.")
        
        with col_status2:
            if st.session_state.get('v2_analise'):
                v2_result = st.session_state['v2_analise']
                st.info(f"📊 {v2_result['frequencia_media']} posts/semana | {v2_result['regularidade']}")
            else:
                st.caption("⏳ Aguardando análise...")
        
        if st.session_state.get('v2_analise'):
            st.markdown("---")
            v2_result = st.session_state['v2_analise']
            exibir_analise_v2(v2_result)
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("✅ Aplicar nota V2", key="aplicar_v2", use_container_width=True):
                    st.session_state['v2'] = int(v2_result['nota_sugerida'])
                    st.session_state['v2_override'] = True
                    st.success(f"✅ V2 ajustado!")

    # V3
    st.markdown("---")
    with st.expander("🏆 Análise de Autoridade (V3)", expanded=False):
        st.markdown("**Como usar:** Use a bio/transcrições do V1 + depoimentos")
        
        depoimentos_arquivos = st.file_uploader(
            "Upload dos depoimentos (.txt)",
            type=['txt'],
            accept_multiple_files=True,
            key="depoimentos_upload"
        )
        depoimentos_manuais_input = st.text_area(
            "Depoimentos (um por linha)",
            placeholder="'Aprendi com o método!'",
            height=100,
            key="depoimentos_input_manual"
        )
        
        if depoimentos_arquivos:
            todas_linhas = extrair_linhas_multiplos_arquivos(depoimentos_arquivos)
            if todas_linhas:
                depoimentos_manuais_input = '\n'.join(todas_linhas)
                st.success(f"✅ {len(todas_linhas)} depoimentos carregados")
        
        col_btn3, col_status3 = st.columns([1, 2])
        
        with col_btn3:
            if st.button("🏆 Analisar V3", key="analisar_v3", use_container_width=True):
                if st.session_state.get('v1_bio') and st.session_state.get('v1_transcricoes'):
                    with st.spinner("Analisando autoridade..."):
                        depoimentos_list = []
                        if depoimentos_manuais_input:
                            depoimentos_list = [d.strip() for d in depoimentos_manuais_input.split('\n') if d.strip()]
                        
                        resultado = analisar_autoridade_v3(
                            st.session_state['v1_bio'],
                            st.session_state['v1_transcricoes'],
                            depoimentos_list
                        )
                        
                        st.session_state['v3_analise'] = resultado
                        st.session_state['v3_nota_sugerida'] = resultado['nota_sugerida']
                        
                        st.success(f"✅ Nota sugerida: {resultado['nota_sugerida']}/10")
                else:
                    st.warning("Analise o V1 primeiro.")
        
        with col_status3:
            if st.session_state.get('v3_analise'):
                v3_result = st.session_state['v3_analise']
                st.info(f"📊 Depoimentos: {v3_result['depoimentos']}")
            else:
                st.caption("⏳ Aguardando análise...")
        
        if st.session_state.get('v3_analise'):
            st.markdown("---")
            v3_result = st.session_state['v3_analise']
            exibir_analise_v3(v3_result)
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("✅ Aplicar nota V3", key="aplicar_v3", use_container_width=True):
                    st.session_state['v3'] = int(v3_result['nota_sugerida'])
                    st.session_state['v3_override'] = True
                    st.success(f"✅ V3 ajustado!")

    # V4
    st.markdown("---")
    with st.expander("💬 Análise de Engajamento (V4)", expanded=False):
        st.markdown("**Como usar:** Faça upload dos comentários (.txt)")
        
        comentarios_arquivos = st.file_uploader(
            "Upload dos comentários (.txt)",
            type=['txt'],
            accept_multiple_files=True,
            key="comentarios_upload"
        )
        comentarios_input = st.text_area(
            "Comentários (um por linha)",
            placeholder="Que aula incrível!",
            height=100,
            key="comentarios_input_manual"
        )
        
        if comentarios_arquivos:
            todas_linhas = extrair_linhas_multiplos_arquivos(comentarios_arquivos)
            if todas_linhas:
                comentarios_input = '\n'.join(todas_linhas)
                st.success(f"✅ {len(todas_linhas)} comentários carregados")
        
        col_btn4, col_status4 = st.columns([1, 2])
        
        with col_btn4:
            if st.button("💬 Analisar V4", key="analisar_v4", use_container_width=True):
                if comentarios_input:
                    comentarios_list = [c.strip() for c in comentarios_input.split('\n') if c.strip()]
                    
                    with st.spinner("Analisando engajamento..."):
                        resultado = analisar_engajamento_v4(comentarios_list)
                        
                        st.session_state['v4_analise'] = resultado
                        st.session_state['v4_nota_sugerida'] = resultado['nota_sugerida']
                        
                        st.success(f"✅ Nota sugerida: {resultado['nota_sugerida']}/10")
                else:
                    st.warning("Preencha pelo menos 3 comentários.")
        
        with col_status4:
            if st.session_state.get('v4_analise'):
                v4_result = st.session_state['v4_analise']
                st.info(f"📊 {v4_result['total_comentarios']} comentários | {v4_result['qualidade']}")
            else:
                st.caption("⏳ Aguardando análise...")
        
        if st.session_state.get('v4_analise'):
            st.markdown("---")
            v4_result = st.session_state['v4_analise']
            exibir_analise_v4(v4_result)
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("✅ Aplicar nota V4", key="aplicar_v4", use_container_width=True):
                    st.session_state['v4'] = int(v4_result['nota_sugerida'])
                    st.session_state['v4_override'] = True
                    st.success(f"✅ V4 ajustado!")

    # V5
    st.markdown("---")
    with st.expander("💰 Análise de Preço (V5)", expanded=False):
        col_preco1, col_preco2 = st.columns(2)
        
        with col_preco1:
            preco_input = st.number_input("💰 Preço (R$)", min_value=0.0, value=0.0, step=10.0, key="preco_input")
        
        with col_preco2:
            preco_mercado_input = st.number_input("📊 Mercado (R$)", min_value=0.0, value=0.0, step=10.0, key="preco_mercado_input")
        
        justificativa_input = st.text_area(
            "📝 Justificativa",
            placeholder="Método exclusivo...",
            height=60,
            key="justificativa_input"
        )
        
        col_btn5, col_status5 = st.columns([1, 2])
        
        with col_btn5:
            if st.button("💰 Analisar V5", key="analisar_v5", use_container_width=True):
                if preco_input > 0:
                    with st.spinner("Analisando preço..."):
                        resultado = analisar_preco_v5(
                            preco_input,
                            preco_mercado_input if preco_mercado_input > 0 else None,
                            justificativa_input
                        )
                        
                        st.session_state['v5_analise'] = resultado
                        st.session_state['v5_nota_sugerida'] = resultado['nota_sugerida']
                        
                        st.success(f"✅ Nota sugerida: {resultado['nota_sugerida']}/10")
                else:
                    st.warning("Informe o preço.")
        
        with col_status5:
            if st.session_state.get('v5_analise'):
                v5_result = st.session_state['v5_analise']
                st.info(f"📊 {v5_result['posicionamento']}")
            else:
                st.caption("⏳ Aguardando análise...")
        
        if st.session_state.get('v5_analise'):
            st.markdown("---")
            v5_result = st.session_state['v5_analise']
            exibir_analise_v5(v5_result)
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("✅ Aplicar nota V5", key="aplicar_v5", use_container_width=True):
                    st.session_state['v5'] = int(v5_result['nota_sugerida'])
                    st.session_state['v5_override'] = True
                    st.success(f"✅ V5 ajustado!")

    # Métricas de negócio
    st.markdown("---")
    st.subheader("📊 Métricas de Negócio")

    seguidores = st.number_input("Seguidores", min_value=0, value=10000, step=1000)
    crescimento = st.number_input("Crescimento mensal (%)", min_value=0.0, value=5.0, step=0.5)
    produtos = st.number_input("Produtos ativos", min_value=0, value=2, step=1)
    canais = st.number_input("Canais ativos", min_value=1, value=3, step=1)
    autoridade = st.checkbox("Autoridade externa validada")

    # Arquétipo
    st.markdown("---")
    st.subheader("🎭 Arquétipo")
    arquétipo = st.selectbox(
        "Classificação qualitativa",
        ["", "Sábio", "Herói", "Mago", "Fora-da-lei", "Amante",
         "Criador", "Governante", "Cuidador", "Explorador",
         "Inocente", "Bobo da Corte", "Cara Comum"],
        index=0
    )

    st.markdown("---")
    if st.button("📘 Abrir Manual do Analista", use_container_width=True):
        st.session_state.mostrar_manual = True

    st.markdown("---")
    analisar = st.button("🔍 Analisar Marca", type="primary", use_container_width=True)


# ============================================================================
# MAIN
# ============================================================================

if st.session_state.get('mostrar_manual', False):
    mostrar_manual()
    st.session_state.mostrar_manual = False

if not analisar:
    st.title("🎯 Branding Analyzer")
    st.markdown("""
    ### Ferramenta científica de análise de branding

    **Base teórica:** Aaker, Keller, Kapferer e Ehrenberg-Bass

    **⚡ MODO AUTOMATIZADO (Nível 1):**
    - Faça upload de **múltiplos arquivos** `.txt` com bio, transcrições, datas e comentários
    - Relatório completo com **gráficos** e **fundamentação teórica**
    - **Recomendações de palavras-chave** baseadas no Google Trends
    """)

    st.subheader("📈 Google Trends — Análise de Mercado")
    
    col_trends1, col_trends2 = st.columns([3, 1])
    
    with col_trends1:
        palavras_trends = st.text_input(
            "Palavras-chave (separadas por vírgula)",
            placeholder="Ex: guitarra, blues, slide guitar",
            key="palavras_trends_input"
        )
    
    with col_trends2:
        if st.button("📊 Buscar Trends", key="buscar_trends_principal", use_container_width=True):
            if palavras_trends:
                lista_palavras = [p.strip() for p in palavras_trends.split(',') if p.strip()]
                
                with st.spinner("Consultando Google Trends..."):
                    resultados = analisar_trends(lista_palavras)
                    
                    if resultados['sucesso']:
                        st.session_state['trends_resultado_principal'] = resultados
                        st.success("✅ Dados do Google Trends carregados!")
                    else:
                        st.error(f"❌ {resultados['mensagem']}")
            else:
                st.warning("Digite pelo menos uma palavra-chave.")
    
    if st.session_state.get('trends_resultado_principal'):
        resultados = st.session_state['trends_resultado_principal']
        
        if resultados['sucesso']:
            dados_tempo = resultados['dados_tempo']
            if 'isPartial' in dados_tempo.columns:
                dados_tempo = dados_tempo.drop(columns=['isPartial'])
            
            if not dados_tempo.empty:
                st.plotly_chart(criar_grafico_trends(dados_tempo), use_container_width=True)
            
            if resultados.get('medias'):
                st.subheader("📊 Estatísticas de Interesse")
                medias_data = []
                for palavra, dados in resultados['medias'].items():
                    medias_data.append({
                        'Palavra': palavra,
                        'Média': dados['media'],
                        'Máximo': dados['maximo'],
                        'Mínimo': dados['minimo'],
                        'Tendência': '📈 Crescendo' if dados['tendencia'] == 'crescendo' else '📉 Diminuindo'
                    })
                st.dataframe(pd.DataFrame(medias_data), use_container_width=True, hide_index=True)

    st.subheader("📝 Atribua ou confirme as notas (0-10)")

    desc_v1 = "0: Sem nicho | 3: Nicho amplo | 5: Nicho comum | 7: Nicho específico | 10: Território exclusivo"
    desc_v2 = "0: Muda constante | 3: Esporádico | 5: Razoável com gaps | 7: Regular | 10: Cadência constante"
    desc_v3 = "0: Nenhuma prova | 3: Menciona | 5: Prova social | 7: Provas consistentes | 10: Validação externa"
    desc_v4 = "0: Genéricos | 3: Raso | 5: Com perguntas | 7: Comunidade ativa | 10: UGC"
    desc_v5 = "0: Incoerente | 3: Descompasso | 5: Aceitável | 7: Coerente | 10: Reforça posicionamento"
    desc_v6 = "0: 1 canal, baixa | 3: 1 canal, razoável | 5: 2 canais | 7: 3+ canais | 10: Multi-canal dominante"
    desc_v7 = "Soma de 5 subcritérios (0-2 cada): Paleta, Vestimenta, Cenário, Qualidade, Marca Visual"

    v1_default = int(st.session_state.get('v1_nota_sugerida', 7))
    v2_default = int(st.session_state.get('v2_nota_sugerida', 7))
    v3_default = int(st.session_state.get('v3_nota_sugerida', 7))
    v4_default = int(st.session_state.get('v4_nota_sugerida', 5))
    v5_default = int(st.session_state.get('v5_nota_sugerida', 7))
    v6_default = int(st.session_state.get('v6', 7))
    v7_default = int(st.session_state.get('v7', 7))

    col1, col2 = st.columns(2)

    with col1:
        v1 = st.slider("V1 — Posicionamento", 0, 10, v1_default, help=desc_v1)
        v2 = st.slider("V2 — Consistência", 0, 10, v2_default, help=desc_v2)
        v3 = st.slider("V3 — Autoridade", 0, 10, v3_default, help=desc_v3)
        v4 = st.slider("V4 — Engajamento", 0, 10, v4_default, help=desc_v4)

    with col2:
        v5 = st.slider("V5 — Preço-Percepção", 0, 10, v5_default, help=desc_v5)
        v6 = st.slider("V6 — Onipresença", 0, 10, v6_default, help=desc_v6)
        v7 = st.slider("V7 — Coerência Visual", 0, 10, v7_default, help=desc_v7)

    st.session_state.v1 = v1
    st.session_state.v2 = v2
    st.session_state.v3 = v3
    st.session_state.v4 = v4
    st.session_state.v5 = v5
    st.session_state.v6 = v6
    st.session_state.v7 = v7

    st.info("💡 Depois de preencher os dados na barra lateral, clique em 'Analisar Marca'")

else:
    v1_final = st.session_state.get('v1', st.session_state.get('v1_nota_sugerida', 7))
    v2_final = st.session_state.get('v2', st.session_state.get('v2_nota_sugerida', 7))
    v3_final = st.session_state.get('v3', st.session_state.get('v3_nota_sugerida', 7))
    v4_final = st.session_state.get('v4', st.session_state.get('v4_nota_sugerida', 5))
    v5_final = st.session_state.get('v5', st.session_state.get('v5_nota_sugerida', 7))
    v6_final = st.session_state.get('v6', 7)
    v7_final = st.session_state.get('v7', 7)
    
    notas = {
        'v1': v1_final,
        'v2': v2_final,
        'v3': v3_final,
        'v4': v4_final,
        'v5': v5_final,
        'v6': v6_final,
        'v7': v7_final
    }

    resultado_score = calcular_score_ponderado(notas, segmento=segmento_key)
    score = resultado_score['score_ponderado']

    dados_marca = {
        'score_total': score,
        'seguidores': seguidores,
        'crescimento_mensal': crescimento,
        'produtos_ativos': produtos,
        'canais_ativos': canais,
        'autoridade_externa': autoridade
    }
    resultado_classificacao = classificar_marca(dados_marca, segmento=segmento_key)
    recomendacoes = gerar_recomendacoes(notas, arquétipo=arquétipo if arquétipo else None)

    st.title(f"📊 {nome_marca or 'Marca não nomeada'}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        emoji = "🏆" if score >= 8 else "📈" if score >= 6.5 else "📊" if score >= 5 else "⚠️"
        st.metric(f"{emoji} Score", f"{score:.1f}/10")

    with col2:
        st.metric("Classificação", resultado_score['classificacao'])

    with col3:
        st.metric("Status", resultado_classificacao['classificacao'])

    with col4:
        st.metric("Arquétipo", arquétipo if arquétipo else "Não definido")

    st.markdown("---")
    st.subheader("📏 Régua de Classificação")

    score_pos = min(score, 10.0)
    faixas = [
        {"label": "⚠️ Risco", "inicio": 0, "fim": 4.9, "cor": "#ef4444", "bg": "#fee2e2"},
        {"label": "📊 Interm.", "inicio": 5.0, "fim": 6.4, "cor": "#f59e0b", "bg": "#fef3c7"},
        {"label": "📈 Forte", "inicio": 6.5, "fim": 7.9, "cor": "#10b981", "bg": "#d1fae5"},
        {"label": "🏆 Premium", "inicio": 8.0, "fim": 10.0, "cor": "#8b5cf6", "bg": "#ede9fe"}
    ]

    faixa_atual = None
    for f in faixas:
        if f["inicio"] <= score_pos <= f["fim"]:
            faixa_atual = f
            break

    percentual = (score_pos / 10) * 100

    col_r1, col_r2 = st.columns([3, 1])

    with col_r1:
        st.markdown(f"""
        <div style="background: linear-gradient(to right, #ef4444 0%, #ef4444 49%, #f59e0b 49%, #f59e0b 64%, #10b981 64%, #10b981 79%, #8b5cf6 79%, #8b5cf6 100%); 
                    height: 24px; 
                    border-radius: 12px; 
                    position: relative;
                    margin: 8px 0;">
            <div style="position: absolute; 
                        left: {percentual}%; 
                        top: -8px; 
                        transform: translateX(-50%);
                        width: 0; 
                        height: 0; 
                        border-left: 10px solid transparent; 
                        border-right: 10px solid transparent; 
                        border-bottom: 14px solid #1f2937;">
            </div>
            <div style="position: absolute; 
                        left: {percentual}%; 
                        top: 10px; 
                        transform: translateX(-50%);
                        background: #1f2937; 
                        color: white; 
                        padding: 2px 10px; 
                        border-radius: 4px;
                        font-size: 14px;
                        font-weight: bold;">
                {score:.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_labels = st.columns(4)
        for i, f in enumerate(faixas):
            with col_labels[i]:
                st.markdown(f"""
                <div style="text-align: center; font-size: 12px; color: #6b7280;">
                    <span style="color: {f['cor']}; font-weight: bold;">{f['label']}</span>
                    <br>{f['inicio']:.0f} - {f['fim']:.1f}
                </div>
                """, unsafe_allow_html=True)

    with col_r2:
        if faixa_atual:
            st.markdown(f"""
            <div style="background: {faixa_atual['bg']}; 
                        padding: 8px 12px; 
                        border-radius: 8px; 
                        text-align: center;
                        border: 2px solid {faixa_atual['cor']};">
                <div style="font-size: 20px; font-weight: bold; color: {faixa_atual['cor']};">
                    {faixa_atual['label']}
                </div>
                <div style="font-size: 12px; color: #6b7280;">
                    {score:.1f}/10
                </div>
            </div>
            """, unsafe_allow_html=True)

    if score >= 8.0:
        st.success("🏆 **Premium** — Marca consolidada!")
    elif score >= 6.5:
        st.info("📈 **Forte** — Marca bem estruturada!")
    elif score >= 5.0:
        st.warning("📊 **Intermediária** — Marca em desenvolvimento.")
    else:
        st.error("⚠️ **Em Risco** — Marca frágil.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Radar do Perfil")
        fig_radar = criar_radar(notas)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        st.subheader("Comparativo")
        fig_barras = criar_barras(notas)
        st.plotly_chart(fig_barras, use_container_width=True)

    st.markdown("---")
    st.subheader("Detalhamento por Variável")

    breakdown_data = []
    for var, info in resultado_score['breakdown'].items():
        breakdown_data.append({
            'Variável': var,
            'Código': info['codigo'],
            'Nota': info['nota'],
            'Peso': info['peso'],
            'Contribuição': info['contribuicao'],
            '% do Score': f"{info['percentual']:.1f}%"
        })

    st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("💡 Recomendações com Fundamentação Teórica")

    st.info(recomendacoes['resumo'])

    if recomendacoes.get('criticas'):
        st.markdown("#### 🔴 Críticas (nota < 5)")
        for item in recomendacoes['criticas']:
            st.warning(f"**{item['variavel']}** (nota {item['nota']}): {item['recomendacao']}")
            teoria = obter_teoria_variavel(item['variavel'])
            if teoria:
                st.caption(f"📚 **Teoria:** {teoria['teoria']}")
                st.caption(f"💡 **Dica:** {teoria['dica']}")

    if recomendacoes.get('importantes'):
        st.markdown("#### 🟡 Melhorar (nota 5-7)")
        for item in recomendacoes['importantes']:
            st.info(f"**{item['variavel']}** (nota {item['nota']}): {item['recomendacao']}")
            teoria = obter_teoria_variavel(item['variavel'])
            if teoria:
                st.caption(f"📚 **Teoria:** {teoria['teoria']}")
                st.caption(f"💡 **Dica:** {teoria['dica']}")

    if recomendacoes.get('otimizacoes'):
        st.markdown("#### 🟢 Otimizações (nota > 7)")
        for item in recomendacoes['otimizacoes']:
            st.success(f"**{item['variavel']}** (nota {item['nota']}): {item['recomendacao']}")
            teoria = obter_teoria_variavel(item['variavel'])
            if teoria:
                st.caption(f"📚 **Teoria:** {teoria['teoria']}")
                st.caption(f"💡 **Dica:** {teoria['dica']}")

    if recomendacoes.get('arquétipo'):
        st.markdown("#### 🎭 Arquétipo")
        a = recomendacoes['arquétipo']
        st.write(f"**Atual:** {a['atual']}")
        st.write(f"**Ação:** {a['acao']}")
        
        dicas = dicas_arquétipo(a['atual'])
        if dicas:
            with st.expander("📌 Dicas de posicionamento"):
                st.markdown(f"""
                **🎯 Posicionamento:** {dicas['posicionamento']}
                
                **📝 Conteúdo:** {dicas['conteudo']}
                
                **💬 Linguagem:** {dicas['linguagem']}
                
                **🎨 Visual:** {dicas['visual']}
                
                **📢 CTA:** {dicas['cta']}
                """)

    st.markdown("---")
    st.subheader("📥 Exportar Laudo")

    dados_export = {
        'marca': {
            'nome': nome_marca,
            'segmento': segmento,
            'seguidores': seguidores,
            'crescimento': crescimento,
            'produtos': produtos,
            'canais': canais,
            'autoridade': autoridade,
            'arquétipo': arquétipo
        },
        'notas': notas,
        'score': resultado_score,
        'classificacao': resultado_classificacao,
        'recomendacoes': recomendacoes,
        'analises_objetivas': {
            'v2': st.session_state.get('v2_analise', {}),
            'v3': st.session_state.get('v3_analise', {}),
            'v4': st.session_state.get('v4_analise', {}),
            'v5': st.session_state.get('v5_analise', {})
        },
        'trends': st.session_state.get('trends_resultado_principal', {}) or st.session_state.get('trends_resultado_resultados', {}),
        'data_analise': datetime.now().isoformat()
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="📄 Baixar Word (.docx)",
            data=gerar_docx(dados_export),
            file_name=f"laudo_{nome_marca or 'marca'}_{datetime.now().strftime('%Y%m%d_%H%M')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with col2:
        st.info("📊 Em breve: Excel")

    with col3:
        st.info("📝 Em breve: Markdown")


st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6b7280; font-size: 0.8rem;">
        Branding Analyzer v1.0 — Baseado em Aaker, Keller, Kapferer e Ehrenberg-Bass
    </div>
    """,
    unsafe_allow_html=True
)
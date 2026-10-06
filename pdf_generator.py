"""
===============================================================================
PDF GENERATOR — Gera o laudo em PDF profissional
===============================================================================
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime


# ============================================================================
# CORES DO BRANDING
# ============================================================================

COR_PRIMARIA = colors.HexColor('#1F2937')      # Azul escuro
COR_SECUNDARIA = colors.HexColor('#2563EB')    # Azul médio
COR_SUCESSO = colors.HexColor('#10B981')       # Verde
COR_ALERTA = colors.HexColor('#F59E0B')        # Amarelo
COR_ERRO = colors.HexColor('#EF4444')          # Vermelho
COR_CINZA = colors.HexColor('#6B7280')         # Cinza
COR_FUNDO_CLARO = colors.HexColor('#F3F4F6')   # Cinza claro


# ============================================================================
# ESTILOS
# ============================================================================

def criar_estilos():
    """Cria estilos customizados para o PDF."""
    styles = getSampleStyleSheet()
    
    estilos = {
        'titulo_capa': ParagraphStyle(
            'TituloCapa',
            parent=styles['Heading1'],
            fontSize=36,
            textColor=COR_PRIMARIA,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ),
        'subtitulo_capa': ParagraphStyle(
            'SubtituloCapa',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=COR_SECUNDARIA,
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica-Oblique'
        ),
        'nome_marca': ParagraphStyle(
            'NomeMarca',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=COR_SECUNDARIA,
            alignment=TA_CENTER,
            spaceAfter=15,
            fontName='Helvetica-Bold'
        ),
        'score_capa': ParagraphStyle(
            'ScoreCapa',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=COR_PRIMARIA,
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ),
        'titulo_secao': ParagraphStyle(
            'TituloSecao',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=COR_PRIMARIA,
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ),
        'subtitulo': ParagraphStyle(
            'Subtitulo',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=COR_SECUNDARIA,
            spaceBefore=10,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ),
        'texto': ParagraphStyle(
            'Texto',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COR_PRIMARIA,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ),
        'texto_pequeno': ParagraphStyle(
            'TextoPequeno',
            parent=styles['BodyText'],
            fontSize=9,
            textColor=COR_CINZA,
            alignment=TA_LEFT
        ),
        'texto_destaque': ParagraphStyle(
            'TextoDestaque',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COR_PRIMARIA,
            alignment=TA_LEFT,
            spaceAfter=4,
            fontName='Helvetica-Bold'
        ),
        'rodape': ParagraphStyle(
            'Rodape',
            parent=styles['BodyText'],
            fontSize=9,
            textColor=COR_CINZA,
            alignment=TA_CENTER
        ),
    }
    
    return estilos


# ============================================================================
# GERADOR DE PDF
# ============================================================================

def gerar_pdf(dados):
    """
    Gera o laudo em PDF profissional.
    
    Args:
        dados: dict com todos os dados da análise
    
    Returns:
        BytesIO com o PDF
    """
    
    buffer = BytesIO()
    
    # Criar documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title='Laudo de Branding',
        author='Branding Analyzer'
    )
    
    estilos = criar_estilos()
    story = []
    
    # ========================================================================
    # CAPA
    # ========================================================================
    
    story.append(Spacer(1, 3*cm))
    
    # Título principal
    story.append(Paragraph('BRANDING ANALYZER', estilos['titulo_capa']))
    story.append(Paragraph('Análise Científica de Branding', estilos['subtitulo_capa']))
    
    story.append(Spacer(1, 1*cm))
    
    # Linha divisória
    linha = Table([['']], colWidths=[16*cm], rowHeights=[2])
    linha.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COR_SECUNDARIA),
    ]))
    story.append(linha)
    
    story.append(Spacer(1, 2*cm))
    
    # Nome da marca
    marca = dados.get('marca', {})
    nome_marca = marca.get('nome', 'Marca não informada')
    story.append(Paragraph(nome_marca, estilos['nome_marca']))
    
    story.append(Spacer(1, 1.5*cm))
    
    # Score e classificação
    score = dados.get('score', {})
    score_valor = score.get('score_ponderado', 0)
    classificacao = score.get('classificacao', 'N/A')
    
    story.append(Paragraph(f'Score: {score_valor}/10', estilos['score_capa']))
    
    # Classificação com cor
    if score_valor >= 6.5:
        cor_class = COR_SUCESSO
    elif score_valor >= 5:
        cor_class = COR_ALERTA
    else:
        cor_class = COR_ERRO
    
    class_style = ParagraphStyle(
        'ClassStyle',
        parent=estilos['score_capa'],
        fontSize=18,
        textColor=cor_class
    )
    story.append(Paragraph(classificacao.upper(), class_style))
    
    story.append(Spacer(1, 4*cm))
    
    # Data
    data_par = Paragraph(
        f'Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}',
        estilos['rodape']
    )
    story.append(data_par)
    
    # Rodapé da capa
    story.append(Paragraph(
        'Baseado em Aaker, Keller, Kapferer e Ehrenberg-Bass',
        estilos['rodape']
    ))
    
    # ========================================================================
    # PÁGINA 2 — DADOS DA MARCA
    # ========================================================================
    story.append(PageBreak())
    
    story.append(Paragraph('1. Dados da Marca', estilos['titulo_secao']))
    
    # Tabela de dados
    dados_tabela = [
        ['Nome:', marca.get('nome', 'Não informado')],
        ['Segmento:', marca.get('segmento', 'Não informado')],
        ['Seguidores:', f"{marca.get('seguidores', 0):,}"],
        ['Crescimento mensal:', f"{marca.get('crescimento', 0)}%/mês"],
        ['Produtos ativos:', str(marca.get('produtos', 0))],
        ['Canais ativos:', str(marca.get('canais', 0))],
        ['Autoridade externa:', 'Sim' if marca.get('autoridade') else 'Não'],
        ['Arquétipo:', marca.get('arquétipo', 'Não definido')],
    ]
    
    tabela = Table(dados_tabela, colWidths=[5*cm, 11*cm])
    tabela.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), COR_PRIMARIA),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, COR_FUNDO_CLARO),
    ]))
    story.append(tabela)
    
    story.append(Spacer(1, 1*cm))
    
    # ========================================================================
    # SEÇÃO 2 — SCORE TOTAL
    # ========================================================================
    story.append(Paragraph('2. Score Total', estilos['titulo_secao']))
    
    story.append(Paragraph(
        f'Score Simples: <b>{score.get("score_simples", "N/A")}/10</b>',
        estilos['texto']
    ))
    story.append(Paragraph(
        f'Score Ponderado: <b>{score.get("score_ponderado", "N/A")}/10</b>',
        estilos['texto']
    ))
    story.append(Paragraph(
        f'Classificação: <b>{score.get("classificacao", "N/A")}</b>',
        estilos['texto']
    ))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Régua visual
    try:
        img_regua = dados.get('grafico_regua')
        if img_regua:
            story.append(Image(img_regua, width=16*cm, height=4*cm))
    except:
        pass
    
    # ========================================================================
    # PÁGINA 3 — GRÁFICOS
    # ========================================================================
    story.append(PageBreak())
    
    story.append(Paragraph('3. Visualização do Perfil', estilos['titulo_secao']))
    
    # Radar
    try:
        img_radar = dados.get('grafico_radar')
        if img_radar:
            story.append(Paragraph('Radar do Perfil', estilos['subtitulo']))
            story.append(Image(img_radar, width=12*cm, height=12*cm))
    except:
        pass
    
    story.append(Spacer(1, 0.5*cm))
    
    # Barras
    try:
        img_barras = dados.get('grafico_barras')
        if img_barras:
            story.append(Paragraph('Comparativo por Variável', estilos['subtitulo']))
            story.append(Image(img_barras, width=16*cm, height=10*cm))
    except:
        pass
    
    # ========================================================================
    # PÁGINA 4 — BREAKDOWN
    # ========================================================================
    story.append(PageBreak())
    
    story.append(Paragraph('4. Detalhamento por Variável', estilos['titulo_secao']))
    
    # Tabela de breakdown
    cabecalhos = ['Variável', 'Código', 'Nota', 'Peso', 'Contrib.', '% Score']
    dados_break = [cabecalhos]
    
    for var, info in score.get('breakdown', {}).items():
        dados_break.append([
            var,
            info.get('codigo', ''),
            str(info.get('nota', 0)),
            str(info.get('peso', 0)),
            str(info.get('contribuicao', 0)),
            f"{info.get('percentual', 0):.1f}%"
        ])
    
    tabela_break = Table(dados_break, colWidths=[4*cm, 2*cm, 1.8*cm, 1.8*cm, 3*cm, 3.4*cm])
    tabela_break.setStyle(TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), COR_PRIMARIA),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        # Dados
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), COR_PRIMARIA),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        # Bordas
        ('GRID', (0, 0), (-1, -1), 0.5, COR_FUNDO_CLARO),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(tabela_break)
    
    # ========================================================================
    # PÁGINA 5 — CLASSIFICAÇÃO
    # ========================================================================
    story.append(PageBreak())
    
    story.append(Paragraph('5. Classificação da Marca', estilos['titulo_secao']))
    
    classificacao_dados = dados.get('classificacao', {})
    story.append(Paragraph(
        f'Status: <b>{classificacao_dados.get("classificacao", "N/A")}</b>',
        estilos['texto']
    ))
    story.append(Paragraph(
        f'Nível: <b>{classificacao_dados.get("nivel", "N/A")}</b>',
        estilos['texto']
    ))
    story.append(Paragraph(
        f'Ação Recomendada: <b>{classificacao_dados.get("acao_recomendada", "N/A")}</b>',
        estilos['texto']
    ))
    
    if classificacao_dados.get('evidencias'):
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph('Evidências Encontradas:', estilos['subtitulo']))
        for e in classificacao_dados['evidencias']:
            story.append(Paragraph(f'• {e}', estilos['texto']))
    
    # ========================================================================
    # PÁGINA 6 — RECOMENDAÇÕES
    # ========================================================================
    story.append(PageBreak())
    
    story.append(Paragraph('6. Recomendações com Fundamentação Teórica', estilos['titulo_secao']))
    
    recomendacoes = dados.get('recomendacoes', {})
    
    story.append(Paragraph(
        f'Resumo: {recomendacoes.get("resumo", "")}',
        estilos['texto']
    ))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Função para exibir item
    def exibir_item(item, cor):
        item_story = []
        
        estilo_var = ParagraphStyle(
            f'Var{item["variavel"]}',
            parent=estilos['texto_destaque'],
            textColor=cor,
            fontSize=12
        )
        
        item_story.append(Paragraph(
            f'● {item["variavel"]} — Nota {item["nota"]}/10',
            estilo_var
        ))
        item_story.append(Paragraph(
            f'• {item["recomendacao"]}',
            estilos['texto']
        ))
        
        # Teoria
        teoria = dados.get('teorias', {}).get(item['variavel'])
        if teoria:
            estilo_teoria = ParagraphStyle(
                'Teoria',
                parent=estilos['texto_pequeno'],
                leftIndent=0.5*cm,
                textColor=COR_CINZA
            )
            item_story.append(Paragraph(
                f'<i>📚 {teoria["teoria"]}</i>',
                estilo_teoria
            ))
            item_story.append(Paragraph(
                f'<i>💡 Dica: {teoria["dica"]}</i>',
                estilo_teoria
            ))
        
        item_story.append(Spacer(1, 0.3*cm))
        return item_story
    
    # Críticas
    if recomendacoes.get('criticas'):
        story.append(Paragraph('🔴 Críticas (nota < 5)', estilos['subtitulo']))
        for item in recomendacoes['criticas']:
            story.extend(exibir_item(item, COR_ERRO))
    
    # Importantes
    if recomendacoes.get('importantes'):
        story.append(Paragraph('🟡 Melhorar (nota 5-7)', estilos['subtitulo']))
        for item in recomendacoes['importantes']:
            story.extend(exibir_item(item, COR_ALERTA))
    
    # Otimizações
    if recomendacoes.get('otimizacoes'):
        story.append(Paragraph('🟢 Otimizações (nota > 7)', estilos['subtitulo']))
        for item in recomendacoes['otimizacoes']:
            story.extend(exibir_item(item, COR_SUCESSO))
    
    # ========================================================================
    # PÁGINA 7 — PALAVRAS-CHAVE (GOOGLE TRENDS)
    # ========================================================================
    trends_dados = dados.get('trends', {})
    if trends_dados and trends_dados.get('sucesso'):
        story.append(PageBreak())
        story.append(Paragraph('7. Palavras-Chave Recomendadas', estilos['titulo_secao']))
        
        recomendacoes_kw = dados.get('recomendacoes_kw', {})
        
        if recomendacoes_kw.get('palavras_em_alta'):
            story.append(Paragraph('🔥 Palavras em Alta', estilos['subtitulo']))
            for item in recomendacoes_kw['palavras_em_alta']:
                story.append(Paragraph(
                    f'• <b>{item["palavra"]}</b> (média: {item["media"]})',
                    estilos['texto']
                ))
        
        if recomendacoes_kw.get('palavras_em_queda'):
            story.append(Paragraph('📉 Palavras em Queda', estilos['subtitulo']))
            for item in recomendacoes_kw['palavras_em_queda']:
                story.append(Paragraph(
                    f'• <b>{item["palavra"]}</b> (média: {item["media"]})',
                    estilos['texto']
                ))
        
        if recomendacoes_kw.get('termos_relacionados'):
            story.append(Paragraph('🔍 Termos Relacionados', estilos['subtitulo']))
            for item in recomendacoes_kw['termos_relacionados']:
                story.append(Paragraph(
                    f'• <b>{item["termo"]}</b> (+{item["crescimento"]})',
                    estilos['texto']
                ))
    
    # ========================================================================
    # RODAPÉ FINAL
    # ========================================================================
    story.append(Spacer(1, 2*cm))
    
    linha_final = Table([['']], colWidths=[16*cm], rowHeights=[1])
    linha_final.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COR_SECUNDARIA),
    ]))
    story.append(linha_final)
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('<b>Branding Analyzer v1.0</b>', estilos['rodape']))
    story.append(Paragraph(
        'Baseado em Aaker, Keller, Kapferer e Ehrenberg-Bass',
        estilos['rodape']
    ))
    story.append(Paragraph(
        f'© {datetime.now().year} — Todos os direitos reservados',
        estilos['rodape']
    ))
    
    # ========================================================================
    # GERAR PDF
    # ========================================================================
    doc.build(story)
    buffer.seek(0)
    return buffer
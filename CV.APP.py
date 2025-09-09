import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Générateur de CV Intelligent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dictionnaire de traductions
TRANSLATIONS = {
    'fr': {
        'title': 'Générateur de CV Intelligent',
        'subtitle': 'Créez un CV professionnel optimisé ATS',
        'choose_template': 'Choisir un modèle',
        'choose_language': 'Langue du CV',
        'personal_info': 'Informations personnelles',
        'name': 'Nom complet',
        'email': 'Email',
        'phone': 'Téléphone',
        'address': 'Adresse',
        'linkedin': 'LinkedIn',
        'github': 'GitHub',
        'professional_summary': 'Résumé professionnel',
        'experience': 'Expérience professionnelle',
        'education': 'Formation',
        'skills': 'Compétences',
        'languages': 'Langues',
        'interests': 'Centres d\'intérêt',
        'job_title': 'Poste',
        'company': 'Entreprise',
        'start_date': 'Date de début',
        'end_date': 'Date de fin',
        'description': 'Description',
        'degree': 'Diplôme',
        'institution': 'Institution',
        'year': 'Année',
        'skill_name': 'Compétence',
        'skill_level': 'Niveau',
        'language_name': 'Langue',
        'language_level': 'Niveau',
        'add_experience': 'Ajouter une expérience',
        'add_education': 'Ajouter une formation',
        'add_skill': 'Ajouter une compétence',
        'add_language': 'Ajouter une langue',
        'preview': 'Aperçu du CV',
        'generate_pdf': 'Générer le PDF',
        'template_classic': 'Classique',
        'template_modern': 'Moderne',
        'template_creative': 'Créatif'
    },
    'en': {
        'title': 'Intelligent CV Generator',
        'subtitle': 'Create a professional ATS-optimized resume',
        'choose_template': 'Choose Template',
        'choose_language': 'CV Language',
        'personal_info': 'Personal Information',
        'name': 'Full Name',
        'email': 'Email',
        'phone': 'Phone',
        'address': 'Address',
        'linkedin': 'LinkedIn',
        'github': 'GitHub',
        'professional_summary': 'Professional Summary',
        'experience': 'Professional Experience',
        'education': 'Education',
        'skills': 'Skills',
        'languages': 'Languages',
        'interests': 'Interests',
        'job_title': 'Job Title',
        'company': 'Company',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'description': 'Description',
        'degree': 'Degree',
        'institution': 'Institution',
        'year': 'Year',
        'skill_name': 'Skill',
        'skill_level': 'Level',
        'language_name': 'Language',
        'language_level': 'Level',
        'add_experience': 'Add Experience',
        'add_education': 'Add Education',
        'add_skill': 'Add Skill',
        'add_language': 'Add Language',
        'preview': 'CV Preview',
        'generate_pdf': 'Generate PDF',
        'template_classic': 'Classic',
        'template_modern': 'Modern',
        'template_creative': 'Creative'
    },
    'nl': {
        'title': 'Intelligente CV Generator',
        'subtitle': 'Maak een professionele ATS-geoptimaliseerde CV',
        'choose_template': 'Kies Template',
        'choose_language': 'CV Taal',
        'personal_info': 'Persoonlijke Informatie',
        'name': 'Volledige Naam',
        'email': 'Email',
        'phone': 'Telefoon',
        'address': 'Adres',
        'linkedin': 'LinkedIn',
        'github': 'GitHub',
        'professional_summary': 'Professionele Samenvatting',
        'experience': 'Werkervaring',
        'education': 'Opleiding',
        'skills': 'Vaardigheden',
        'languages': 'Talen',
        'interests': 'Interesses',
        'job_title': 'Functie',
        'company': 'Bedrijf',
        'start_date': 'Startdatum',
        'end_date': 'Einddatum',
        'description': 'Beschrijving',
        'degree': 'Diploma',
        'institution': 'Instelling',
        'year': 'Jaar',
        'skill_name': 'Vaardigheid',
        'skill_level': 'Niveau',
        'language_name': 'Taal',
        'language_level': 'Niveau',
        'add_experience': 'Ervaring Toevoegen',
        'add_education': 'Opleiding Toevoegen',
        'add_skill': 'Vaardigheid Toevoegen',
        'add_language': 'Taal Toevoegen',
        'preview': 'CV Voorvertoning',
        'generate_pdf': 'PDF Genereren',
        'template_classic': 'Klassiek',
        'template_modern': 'Modern',
        'template_creative': 'Creatief'
    }
}

# Initialisation des variables de session
if 'cv_data' not in st.session_state:
    st.session_state.cv_data = {
        'personal_info': {},
        'professional_summary': '',
        'experiences': [],
        'education': [],
        'skills': [],
        'languages': [],
        'interests': ''
    }

if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'fr'

if 'selected_template' not in st.session_state:
    st.session_state.selected_template = 'classic'

def get_text(key):
    """Récupère le texte traduit selon la langue sélectionnée"""
    return TRANSLATIONS[st.session_state.selected_language].get(key, key)

def create_pdf(cv_data, template, language):
    """Génère un PDF du CV avec le style choisi"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=12,
        textColor=colors.HexColor('#2C3E50'),
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.HexColor('#34495E'),
        borderWidth=1,
        borderColor=colors.HexColor('#BDC3C7'),
        borderPadding=5
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    story = []
    
    # En-tête avec nom
    if cv_data['personal_info'].get('name'):
        story.append(Paragraph(cv_data['personal_info']['name'], title_style))
    
    # Informations de contact
    contact_info = []
    if cv_data['personal_info'].get('email'):
        contact_info.append(f"Email: {cv_data['personal_info']['email']}")
    if cv_data['personal_info'].get('phone'):
        contact_info.append(f"Téléphone: {cv_data['personal_info']['phone']}")
    if cv_data['personal_info'].get('address'):
        contact_info.append(f"Adresse: {cv_data['personal_info']['address']}")
    if cv_data['personal_info'].get('linkedin'):
        contact_info.append(f"LinkedIn: {cv_data['personal_info']['linkedin']}")
    
    if contact_info:
        story.append(Paragraph(" | ".join(contact_info), normal_style))
    
    story.append(Spacer(1, 12))
    
    # Résumé professionnel
    if cv_data.get('professional_summary'):
        story.append(Paragraph(get_text('professional_summary'), heading_style))
        story.append(Paragraph(cv_data['professional_summary'], normal_style))
    
    # Expérience professionnelle
    if cv_data.get('experiences'):
        story.append(Paragraph(get_text('experience'), heading_style))
        for exp in cv_data['experiences']:
            exp_title = f"<b>{exp.get('job_title', '')} - {exp.get('company', '')}</b>"
            if exp.get('start_date') and exp.get('end_date'):
                exp_title += f" ({exp['start_date']} - {exp['end_date']})"
            story.append(Paragraph(exp_title, normal_style))
            if exp.get('description'):
                story.append(Paragraph(exp['description'], normal_style))
            story.append(Spacer(1, 6))
    
    # Formation
    if cv_data.get('education'):
        story.append(Paragraph(get_text('education'), heading_style))
        for edu in cv_data['education']:
            edu_title = f"<b>{edu.get('degree', '')} - {edu.get('institution', '')}</b>"
            if edu.get('year'):
                edu_title += f" ({edu['year']})"
            story.append(Paragraph(edu_title, normal_style))
            story.append(Spacer(1, 6))
    
    # Compétences
    if cv_data.get('skills'):
        story.append(Paragraph(get_text('skills'), heading_style))
        skills_text = " • ".join([f"{skill['name']} ({skill['level']})" for skill in cv_data['skills']])
        story.append(Paragraph(skills_text, normal_style))
    
    # Langues
    if cv_data.get('languages'):
        story.append(Paragraph(get_text('languages'), heading_style))
        languages_text = " • ".join([f"{lang['name']} ({lang['level']})" for lang in cv_data['languages']])
        story.append(Paragraph(languages_text, normal_style))
    
    # Centres d'intérêt
    if cv_data.get('interests'):
        story.append(Paragraph(get_text('interests'), heading_style))
        story.append(Paragraph(cv_data['interests'], normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    # Titre principal
    st.title("📄 " + get_text('title'))
    st.subheader(get_text('subtitle'))
    
    # Sidebar pour les paramètres
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Sélection de la langue
        language_options = {
            'Français': 'fr',
            'English': 'en',
            'Nederlands': 'nl'
        }
        selected_lang = st.selectbox(
            get_text('choose_language'),
            options=list(language_options.keys()),
            index=0
        )
        st.session_state.selected_language = language_options[selected_lang]
        
        # Sélection du modèle
        template_options = {
            get_text('template_classic'): 'classic',
            get_text('template_modern'): 'modern',
            get_text('template_creative'): 'creative'
        }
        selected_template = st.selectbox(
            get_text('choose_template'),
            options=list(template_options.keys())
        )
        st.session_state.selected_template = template_options[selected_template]
    
    # Interface principale avec colonnes
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("✏️ Saisie des informations")
        
        # Informations personnelles
        with st.expander(get_text('personal_info'), expanded=True):
            st.session_state.cv_data['personal_info']['name'] = st.text_input(get_text('name'))
            st.session_state.cv_data['personal_info']['email'] = st.text_input(get_text('email'))
            st.session_state.cv_data['personal_info']['phone'] = st.text_input(get_text('phone'))
            st.session_state.cv_data['personal_info']['address'] = st.text_area(get_text('address'), height=80)
            st.session_state.cv_data['personal_info']['linkedin'] = st.text_input(get_text('linkedin'))
            st.session_state.cv_data['personal_info']['github'] = st.text_input(get_text('github'))
        
        # Résumé professionnel
        with st.expander(get_text('professional_summary')):
            st.session_state.cv_data['professional_summary'] = st.text_area(
                get_text('professional_summary'),
                height=100,
                placeholder="Décrivez brièvement votre profil professionnel..."
            )
        
        # Expérience professionnelle
        with st.expander(get_text('experience')):
            if st.button(get_text('add_experience')):
                st.session_state.cv_data['experiences'].append({
                    'job_title': '',
                    'company': '',
                    'start_date': '',
                    'end_date': '',
                    'description': ''
                })
            
            for i, exp in enumerate(st.session_state.cv_data['experiences']):
                st.write(f"**Expérience {i+1}**")
                col_a, col_b = st.columns(2)
                with col_a:
                    exp['job_title'] = st.text_input(get_text('job_title'), key=f"job_title_{i}", value=exp.get('job_title', ''))
                    exp['start_date'] = st.text_input(get_text('start_date'), key=f"start_date_{i}", value=exp.get('start_date', ''))
                with col_b:
                    exp['company'] = st.text_input(get_text('company'), key=f"company_{i}", value=exp.get('company', ''))
                    exp['end_date'] = st.text_input(get_text('end_date'), key=f"end_date_{i}", value=exp.get('end_date', ''))
                exp['description'] = st.text_area(get_text('description'), key=f"desc_{i}", value=exp.get('description', ''))
                if st.button(f"Supprimer", key=f"del_exp_{i}"):
                    st.session_state.cv_data['experiences'].pop(i)
                    st.rerun()
                st.divider()
        
        # Formation
        with st.expander(get_text('education')):
            if st.button(get_text('add_education')):
                st.session_state.cv_data['education'].append({
                    'degree': '',
                    'institution': '',
                    'year': ''
                })
            
            for i, edu in enumerate(st.session_state.cv_data['education']):
                st.write(f"**Formation {i+1}**")
                col_a, col_b = st.columns(2)
                with col_a:
                    edu['degree'] = st.text_input(get_text('degree'), key=f"degree_{i}", value=edu.get('degree', ''))
                with col_b:
                    edu['institution'] = st.text_input(get_text('institution'), key=f"institution_{i}", value=edu.get('institution', ''))
                edu['year'] = st.text_input(get_text('year'), key=f"year_{i}", value=edu.get('year', ''))
                if st.button(f"Supprimer", key=f"del_edu_{i}"):
                    st.session_state.cv_data['education'].pop(i)
                    st.rerun()
                st.divider()
        
        # Compétences
        with st.expander(get_text('skills')):
            if st.button(get_text('add_skill')):
                st.session_state.cv_data['skills'].append({
                    'name': '',
                    'level': 'Débutant'
                })
            
            for i, skill in enumerate(st.session_state.cv_data['skills']):
                col_a, col_b = st.columns(2)
                with col_a:
                    skill['name'] = st.text_input(get_text('skill_name'), key=f"skill_{i}", value=skill.get('name', ''))
                with col_b:
                    skill['level'] = st.selectbox(
                        get_text('skill_level'),
                        ['Débutant', 'Intermédiaire', 'Avancé', 'Expert'],
                        key=f"skill_level_{i}",
                        index=['Débutant', 'Intermédiaire', 'Avancé', 'Expert'].index(skill.get('level', 'Débutant'))
                    )
                if st.button(f"Supprimer", key=f"del_skill_{i}"):
                    st.session_state.cv_data['skills'].pop(i)
                    st.rerun()
        
        # Langues
        with st.expander(get_text('languages')):
            if st.button(get_text('add_language')):
                st.session_state.cv_data['languages'].append({
                    'name': '',
                    'level': 'A1'
                })
            
            for i, lang in enumerate(st.session_state.cv_data['languages']):
                col_a, col_b = st.columns(2)
                with col_a:
                    lang['name'] = st.text_input(get_text('language_name'), key=f"lang_{i}", value=lang.get('name', ''))
                with col_b:
                    lang['level'] = st.selectbox(
                        get_text('language_level'),
                        ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Natif'],
                        key=f"lang_level_{i}",
                        index=['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Natif'].index(lang.get('level', 'A1'))
                    )
                if st.button(f"Supprimer", key=f"del_lang_{i}"):
                    st.session_state.cv_data['languages'].pop(i)
                    st.rerun()
        
        # Centres d'intérêt
        with st.expander(get_text('interests')):
            st.session_state.cv_data['interests'] = st.text_area(
                get_text('interests'),
                height=80,
                placeholder="Vos hobbies et centres d'intérêt..."
            )
    
    with col2:
        st.header("👁️ " + get_text('preview'))
        
        # Aperçu du CV
        preview_container = st.container()
        
        with preview_container:
            # Affichage de l'aperçu
            if st.session_state.cv_data['personal_info'].get('name'):
                st.markdown(f"# {st.session_state.cv_data['personal_info']['name']}")
                
                # Informations de contact
                contact_info = []
                for field in ['email', 'phone', 'address', 'linkedin']:
                    if st.session_state.cv_data['personal_info'].get(field):
                        contact_info.append(st.session_state.cv_data['personal_info'][field])
                
                if contact_info:
                    st.markdown(" | ".join(contact_info))
                
                # Résumé professionnel
                if st.session_state.cv_data.get('professional_summary'):
                    st.markdown(f"## {get_text('professional_summary')}")
                    st.markdown(st.session_state.cv_data['professional_summary'])
                
                # Expérience
                if st.session_state.cv_data.get('experiences'):
                    st.markdown(f"## {get_text('experience')}")
                    for exp in st.session_state.cv_data['experiences']:
                        if exp.get('job_title') and exp.get('company'):
                            title = f"**{exp['job_title']} - {exp['company']}**"
                            if exp.get('start_date') and exp.get('end_date'):
                                title += f" ({exp['start_date']} - {exp['end_date']})"
                            st.markdown(title)
                            if exp.get('description'):
                                st.markdown(exp['description'])
                
                # Formation
                if st.session_state.cv_data.get('education'):
                    st.markdown(f"## {get_text('education')}")
                    for edu in st.session_state.cv_data['education']:
                        if edu.get('degree') and edu.get('institution'):
                            title = f"**{edu['degree']} - {edu['institution']}**"
                            if edu.get('year'):
                                title += f" ({edu['year']})"
                            st.markdown(title)
                
                # Compétences
                if st.session_state.cv_data.get('skills'):
                    st.markdown(f"## {get_text('skills')}")
                    skills_list = [f"{skill['name']} ({skill['level']})" for skill in st.session_state.cv_data['skills'] if skill.get('name')]
                    st.markdown(" • ".join(skills_list))
                
                # Langues
                if st.session_state.cv_data.get('languages'):
                    st.markdown(f"## {get_text('languages')}")
                    langs_list = [f"{lang['name']} ({lang['level']})" for lang in st.session_state.cv_data['languages'] if lang.get('name')]
                    st.markdown(" • ".join(langs_list))
                
                # Centres d'intérêt
                if st.session_state.cv_data.get('interests'):
                    st.markdown(f"## {get_text('interests')}")
                    st.markdown(st.session_state.cv_data['interests'])
        
        # Bouton de génération PDF
        st.markdown("---")
        if st.button(get_text('generate_pdf'), type="primary"):
            try:
                pdf_buffer = create_pdf(
                    st.session_state.cv_data,
                    st.session_state.selected_template,
                    st.session_state.selected_language
                )
                
                st.download_button(
                    label="📄 Télécharger le CV (PDF)",
                    data=pdf_buffer,
                    file_name=f"CV_{st.session_state.cv_data['personal_info'].get('name', 'CV')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ CV généré avec succès!")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération du PDF: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Générateur de CV intelligent - Optimisé pour les systèmes ATS*")

if __name__ == "__main__":
    main()
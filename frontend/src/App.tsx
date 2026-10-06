import React from 'react'
import { useTranslation } from 'react-i18next'

const equipment = [
  { id:'VMA-0248', name:'Meuleuse angulaire', place:'Chantier WTECEWA31', control:'12/10/2026', state:'À contrôler', tone:'warning' },
  { id:'VMA-0314', name:'Marteau-piqueur', place:'Camionnette 2-ABC-123', control:'28/11/2026', state:'Conforme', tone:'ok' },
  { id:'VMA-0187', name:'Manomètre digital', place:'Atelier LLN', control:'Échu', state:'NOK', tone:'danger' },
  { id:'VMA-0421', name:'Perceuse-visseuse', place:'Stock Jumet', control:'15/01/2027', state:'Conforme', tone:'ok' },
]

function translateDemoPlace(value: string, lang: string) {
  const map: Record<string, Record<string,string>> = {
    en: {'Chantier WTECEWA31':'Worksite WTECEWA31','Camionnette 2-ABC-123':'Van 2-ABC-123','Atelier LLN':'LLN workshop','Stock Jumet':'Jumet stock'},
    nl: {'Chantier WTECEWA31':'Werf WTECEWA31','Camionnette 2-ABC-123':'Bestelwagen 2-ABC-123','Atelier LLN':'Werkplaats LLN','Stock Jumet':'Voorraad Jumet'},
    pl: {'Chantier WTECEWA31':'Budowa WTECEWA31','Camionnette 2-ABC-123':'Pojazd 2-ABC-123','Atelier LLN':'Warsztat LLN','Stock Jumet':'Magazyn Jumet'}
  }
  return map[lang]?.[value] ?? value
}
function translateDemoControl(value: string, lang: string) {
  if (value !== 'Échu') return value
  return ({en:'Overdue',nl:'Vervallen',pl:'Po terminie'} as Record<string,string>)[lang] ?? value
}
function translateDemoState(value: string, lang: string) {
  const map: Record<string, Record<string,string>> = {
    en:{'À contrôler':'To inspect','Conforme':'Compliant'},
    nl:{'À contrôler':'Te controleren','Conforme':'Conform'},
    pl:{'À contrôler':'Do kontroli','Conforme':'Zgodny'}
  }
  return map[lang]?.[value] ?? value
}

function LanguageFlag({ code }: { code: string }) {
  if (code === 'fr') return <svg viewBox="0 0 30 20" aria-hidden="true"><path fill="#002395" d="M0 0h10v20H0z"/><path fill="#fff" d="M10 0h10v20H10z"/><path fill="#ED2939" d="M20 0h10v20H20z"/></svg>
  if (code === 'nl') return <svg viewBox="0 0 30 20" aria-hidden="true"><path fill="#AE1C28" d="M0 0h30v6.67H0z"/><path fill="#fff" d="M0 6.67h30v6.66H0z"/><path fill="#21468B" d="M0 13.33h30V20H0z"/></svg>
  if (code === 'pl') return <svg viewBox="0 0 30 20" aria-hidden="true"><path fill="#fff" d="M0 0h30v10H0z"/><path fill="#DC143C" d="M0 10h30v10H0z"/></svg>
  return <svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#012169"/><path stroke="#fff" strokeWidth="4" d="M0 0l30 20M30 0L0 20"/><path stroke="#C8102E" strokeWidth="2" d="M0 0l30 20M30 0L0 20"/><path stroke="#fff" strokeWidth="6" d="M15 0v20M0 10h30"/><path stroke="#C8102E" strokeWidth="3.5" d="M15 0v20M0 10h30"/></svg>
}

function App() {
  const { t, i18n } = useTranslation()
  const changeLanguage = (language: string) => {
    void i18n.changeLanguage(language)
    localStorage.setItem('tooly_language', language)
  }
  return <div className="shell">
    <aside>
      <div className="brand"><span className="brandMark">T</span><div><b>Tooly</b><small>{t('equipmentManagement')}</small></div></div>
      <nav>
        <button className="active">⌂ <span>{t('dashboard')}</span></button>
        <button>▣ <span>{t('equipment')}</span></button>
        <button>⌖ <span>{t('worksites')}</span></button>
        <button>✓ <span>{t('inspections')}</span><em>12</em></button>
        <button>⇄ <span>{t('movements')}</span></button>
        <button>▤ <span>{t('documents')}</span></button>
        <button>◇ <span>{t('products')}</span></button>
      </nav>
      <div className="asideBottom"><button>⚙ <span>{t('admin')}</span></button><div className="profile"><span>CC</span><div><b>Cédric C.</b><small>Administrateur</small></div></div></div>
    </aside>
    <main>
      <header><div><h1>{t('hello')}</h1><p>{t('overview')}</p></div><div className="topSelectors"><label>{t('entity')} <select defaultValue="VMA Sud"><option>VMA Sud</option><option>VMA Nord</option><option>BE Maintenance</option></select></label><div className="languages">{[{code:'fr',label:'Français'},{code:'nl',label:'Nederlands'},{code:'en',label:'English'},{code:'pl',label:'Polski'}].map(item=><button key={item.code} title={item.label} aria-label={item.label} className={i18n.language===item.code?'selected':''} onClick={()=>changeLanguage(item.code)}><LanguageFlag code={item.code}/></button>)}</div></div><div className="headerActions"><button className="scan">⌗ {t('scan')}</button><button className="add">+ {t('newEquipment')}</button></div></header>
      <section className="search"><span>⌕</span><input placeholder={t('search')}/></section>
      <section className="metrics">
        <article><span className="metricIcon">▣</span><div><small>{t('active')}</small><strong>1 284</strong><p>+ 18 ce mois</p></div></article>
        <article><span className="metricIcon warn">◷</span><div><small>{t('toInspect')}</small><strong>37</strong><p>12 dans les 7 jours</p></div></article>
        <article><span className="metricIcon danger">!</span><div><small>{t('quarantine')}</small><strong>8</strong><p>3 actions en attente</p></div></article>
        <article><span className="metricIcon good">✓</span><div><small>{t('compliance')}</small><strong>96,8 %</strong><p>1 239 en ordre</p></div></article>
      </section>
      <section className="contentGrid">
        <div className="panel wide"><div className="panelHead"><div><h2>{t('equipment')} à suivre</h2><p>{t('priority')}</p></div><button>{t('seeAll')} →</button></div>
          <div className="table"><div className="tr th"><span>ÉQUIPEMENT</span><span>{t('location')}</span><span>{t('nextInspection')}</span><span>{t('status')}</span><span></span></div>
          {equipment.map(e=><div className="tr" key={e.id}><span><b>{e.name}</b><small>{e.id}</small></span><span>{translateDemoPlace(e.place, i18n.language)}</span><span>{translateDemoControl(e.control, i18n.language)}</span><span><i className={'pill '+e.tone}>{translateDemoState(e.state, i18n.language)}</i></span><span className="arrow">›</span></div>)}</div>
        </div>
        <div className="panel"><div className="panelHead"><div><h2>{t('inspections')}</h2><p>30 prochains jours</p></div></div>
          <div className="ring"><div><strong>37</strong><small>à traiter</small></div></div>
          <div className="legend"><p><i className="dot danger"></i><span>Échus</span><b>9</b></p><p><i className="dot warning"></i><span>≤ 7 jours</span><b>12</b></p><p><i className="dot"></i><span>8–30 jours</span><b>16</b></p></div>
          <button className="primaryFull">{t('openRound')}</button>
        </div>
      </section>
      <section className="panel quick"><div><h2>{t('quick')}</h2><p>{t('quickSub')}</p></div><div className="quickActions"><button><b>⌗</b><span>{t('identify')}<small>{t('identifySub')}</small></span></button><button><b>✓</b><span>{t('doInspection')}<small>{t('doInspectionSub')}</small></span></button><button><b>⇄</b><span>{t('assign')}<small>{t('assignSub')}</small></span></button><button><b>▤</b><span>{t('openSds')}<small>{t('openSdsSub')}</small></span></button></div></section>
    </main>
  </div>
}
export default App

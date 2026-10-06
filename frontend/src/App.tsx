import React from 'react'
import { useTranslation } from 'react-i18next'

const equipment = [
  { id:'VMA-0248', name:'Meuleuse angulaire', place:'Chantier WTECEWA31', control:'12/10/2026', state:'À contrôler', tone:'warning' },
  { id:'VMA-0314', name:'Marteau-piqueur', place:'Camionnette 2-ABC-123', control:'28/11/2026', state:'Conforme', tone:'ok' },
  { id:'VMA-0187', name:'Manomètre digital', place:'Atelier LLN', control:'Échu', state:'NOK', tone:'danger' },
  { id:'VMA-0421', name:'Perceuse-visseuse', place:'Stock Jumet', control:'15/01/2027', state:'Conforme', tone:'ok' },
]

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
      <header><div><h1>{t('hello')}</h1><p>{t('overview')}</p></div><div className="topSelectors"><label>{t('entity')} <select defaultValue="VMA Sud"><option>VMA Sud</option><option>VMA Nord</option><option>BE Maintenance</option></select></label><div className="languages">{['fr','nl','en','pl'].map(lang=><button key={lang} className={i18n.language===lang?'selected':''} onClick={()=>changeLanguage(lang)}>{lang.toUpperCase()}</button>)}</div></div><div className="headerActions"><button className="scan">⌗ {t('scan')}</button><button className="add">+ {t('newEquipment')}</button></div></header>
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
          {equipment.map(e=><div className="tr" key={e.id}><span><b>{e.name}</b><small>{e.id}</small></span><span>{e.place}</span><span>{e.control}</span><span><i className={'pill '+e.tone}>{e.state}</i></span><span className="arrow">›</span></div>)}</div>
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

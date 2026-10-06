import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'

const equipment = [
  { id:'VMA-0248', name:'Meuleuse angulaire', place:'Chantier WTECEWA31', control:'12/10/2026', state:'À contrôler', tone:'warning' },
  { id:'VMA-0314', name:'Marteau-piqueur', place:'Camionnette 2-ABC-123', control:'28/11/2026', state:'Conforme', tone:'ok' },
  { id:'VMA-0187', name:'Manomètre digital', place:'Atelier LLN', control:'Échu', state:'NOK', tone:'danger' },
  { id:'VMA-0421', name:'Perceuse-visseuse', place:'Stock Jumet', control:'15/01/2027', state:'Conforme', tone:'ok' },
]

function LanguageFlag({ code }: { code: string }) {
  if (code === 'fr') return <svg viewBox="0 0 30 20" aria-hidden="true"><path fill="#002395" d="M0 0h10v20H0z"/><path fill="#fff" d="M10 0h10v20H10z"/><path fill="#ED2939" d="M20 0h10v20H20z"/></svg>
  if (code === 'nl') return <svg viewBox="0 0 30 20" aria-hidden="true"><path fill="#AE1C28" d="M0 0h30v6.67H0z"/><path fill="#fff" d="M0 6.67h30v6.66H0z"/><path fill="#21468B" d="M0 13.33h30V20H0z"/></svg>
  if (code === 'pl') return <svg viewBox="0 0 30 20" aria-hidden="true"><path fill="#fff" d="M0 0h30v10H0z"/><path fill="#DC143C" d="M0 10h30v10H0z"/></svg>
  return <svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#012169"/><path stroke="#fff" strokeWidth="4" d="M0 0l30 20M30 0L0 20"/><path stroke="#C8102E" strokeWidth="2" d="M0 0l30 20M30 0L0 20"/><path stroke="#fff" strokeWidth="6" d="M15 0v20M0 10h30"/><path stroke="#C8102E" strokeWidth="3.5" d="M15 0v20M0 10h30"/></svg>
}

function App() {
  const { t, i18n } = useTranslation()
  const [page, setPage] = useState<'dashboard'|'equipment'>('dashboard')
  const changeLanguage = (language: string) => {
    void i18n.changeLanguage(language)
    localStorage.setItem('tooly_language', language)
  }
  return <div className="shell">
    <aside>
      <div className="brand"><span className="brandMark">T</span><div><b>Tooly</b><small>{t('equipmentManagement')}</small></div></div>
      <nav>
        <button className={page==='dashboard'?'active':''} onClick={()=>setPage('dashboard')}>⌂ <span>{t('dashboard')}</span></button>
        <button className={page==='equipment'?'active':''} onClick={()=>setPage('equipment')}>▣ <span>{t('equipment')}</span></button>
        <button>⌖ <span>{t('worksites')}</span></button>
        <button>✓ <span>{t('inspections')}</span><em>12</em></button>
        <button>⇄ <span>{t('movements')}</span></button>
        <button>▤ <span>{t('documents')}</span></button>
        <button>◇ <span>{t('products')}</span></button>
      </nav>
      <div className="asideBottom"><button>⚙ <span>{t('admin')}</span></button><div className="profile"><span>CC</span><div><b>Cédric C.</b><small>Administrateur</small></div></div></div>
    </aside>
    {page === 'dashboard' ? <main>
      <header><div><h1>{t('hello')}</h1><p>{t('overview')}</p></div><div className="topSelectors"><label>{t('entity')} <select defaultValue="VMA Sud"><option>VMA Sud</option><option>VMA Nord</option><option>BE Maintenance</option></select></label><div className="languages">{[{code:'fr',label:'Français'},{code:'nl',label:'Nederlands'},{code:'en',label:'English'},{code:'pl',label:'Polski'}].map(item=><button key={item.code} title={item.label} aria-label={item.label} className={i18n.language===item.code?'selected':''} onClick={()=>changeLanguage(item.code)}><LanguageFlag code={item.code}/></button>)}</div></div><div className="headerActions"><button className="scan">⌗ {t('scan')}</button><button className="add">+ {t('newEquipment')}</button></div></header>
      <section className="search"><span>⌕</span><input placeholder={t('search')}/></section>
      <section className="metrics">
        <article><span className="metricIcon">▣</span><div><small>{t('active')}</small><strong>1 284</strong><p>{t('addedThisMonth', { count: 18 })}</p></div></article>
        <article><span className="metricIcon warn">◷</span><div><small>{t('toInspect')}</small><strong>37</strong><p>{t('within7Days', { count: 12 })}</p></div></article>
        <article><span className="metricIcon danger">!</span><div><small>{t('quarantine')}</small><strong>8</strong><p>{t('pendingActions', { count: 3 })}</p></div></article>
        <article><span className="metricIcon good">✓</span><div><small>{t('compliance')}</small><strong>96,8 %</strong><p>{t('inOrder', { count: '1 239' })}</p></div></article>
      </section>
      <section className="contentGrid">
        <div className="panel wide"><div className="panelHead"><div><h2>{t('equipment')} à suivre</h2><p>{t('priority')}</p></div><button>{t('seeAll')} →</button></div>
          <div className="table"><div className="tr th"><span>ÉQUIPEMENT</span><span>{t('location')}</span><span>{t('nextInspection')}</span><span>{t('status')}</span><span></span></div>
          {equipment.map(e=><div className="tr" key={e.id}><span><b>{t(`demo.${e.id}.name`)}</b><small>{e.id}</small></span><span>{t(`demo.${e.id}.place`)}</span><span>{e.control === 'Échu' ? t('expired') : e.control}</span><span><i className={'pill '+e.tone}>{e.state === 'À contrôler' ? t('due') : e.state === 'Conforme' ? t('compliant') : e.state}</i></span><span className="arrow">›</span></div>)}</div>
        </div>
        <div className="panel"><div className="panelHead"><div><h2>{t('inspections')}</h2><p>{t('next30Days')}</p></div></div>
          <div className="ring"><div><strong>37</strong><small>{t('toHandle')}</small></div></div>
          <div className="legend"><p><i className="dot danger"></i><span>{t('overdue')}</span><b>9</b></p><p><i className="dot warning"></i><span>{t('days7')}</span><b>12</b></p><p><i className="dot"></i><span>{t('days30')}</span><b>16</b></p></div>
          <button className="primaryFull">{t('openRound')}</button>
        </div>
      </section>
      <section className="panel quick"><div><h2>{t('quick')}</h2><p>{t('quickSub')}</p></div><div className="quickActions"><button><b>⌗</b><span>{t('identify')}<small>{t('identifySub')}</small></span></button><button><b>✓</b><span>{t('doInspection')}<small>{t('doInspectionSub')}</small></span></button><button><b>⇄</b><span>{t('assign')}<small>{t('assignSub')}</small></span></button><button><b>▤</b><span>{t('openSds')}<small>{t('openSdsSub')}</small></span></button></div></section>
</main> : <>    <main>
      <header><div><h1>{t('equipment')}</h1><p>{t('equipmentListSub')}</p></div><div className="topSelectors"><label>{t('entity')} <select defaultValue="VMA Sud"><option>VMA Sud</option><option>VMA Nord</option><option>BE Maintenance</option></select></label><div className="languages">{[{code:'fr',label:'Français'},{code:'nl',label:'Nederlands'},{code:'en',label:'English'},{code:'pl',label:'Polski'}].map(item=><button key={item.code} title={item.label} aria-label={item.label} className={i18n.language===item.code?'selected':''} onClick={()=>changeLanguage(item.code)}><LanguageFlag code={item.code}/></button>)}</div></div><div className="headerActions"><button className="scan">⌗ {t('scan')}</button><button className="add">+ {t('newEquipment')}</button></div></header>
      <section className="search"><span>⌕</span><input placeholder={t('search')}/></section>
      <section className="equipmentToolbar"><div className="filterGroup"><button className="filterActive">{t('all')} <b>1284</b></button><button>{t('toInspect')} <b>37</b></button><button>{t('quarantine')} <b>8</b></button><button>{t('lost')} <b>5</b></button></div><button className="filters">☷ {t('filters')}</button></section>
      <section className="panel equipmentPanel"><div className="equipmentTable">
        <div className="eqRow eqHead"><span>{t('number')}</span><span>{t('equipment')}</span><span>{t('category')}</span><span>{t('location')}</span><span>{t('complianceLabel')}</span><span>{t('nextInspection')}</span><span></span></div>
        {equipment.map(e=><div className="eqRow" key={e.id}><span><b>{e.id}</b><small>{t('demoSerial')}</small></span><span><b>{t(`demo.${e.id}.name`)}</b><small>{t('demoBrand')}</small></span><span>{t('portableTool')}</span><span>{t(`demo.${e.id}.place`)}</span><span><i className={'pill '+e.tone}>{e.state==='À contrôler'?t('due'):e.state==='Conforme'?t('compliant'):e.state}</i></span><span>{e.control==='Échu'?t('expired'):e.control}</span><span className="arrow">›</span></div>)}
      </div><div className="tableFooter"><span>{t('showing', {shown:4,total:'1 284'})}</span><div><button disabled>‹</button><button className="pageActive">1</button><button>2</button><button>3</button><button>…</button><button>321</button><button>›</button></div></div></section>
    </main></>}
  </div>
}
export default App

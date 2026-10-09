import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { resolveInspectionTemplate, genericTemplate, meuleuseTemplate } from './inspectionTemplates'

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
  const [page, setPage] = useState<'dashboard'|'equipment'|'equipmentDetail'|'inspection'>('dashboard')
  const [selectedEquipmentId, setSelectedEquipmentId] = useState('VMA-0248')
  const selectedEquipment = equipment.find(item => item.id === selectedEquipmentId) ?? equipment[0]
  const [worksite, setWorksite] = useState('WTECEWA31')
  const [holder, setHolder] = useState('Marc Dupont')
  const [assignmentSaved, setAssignmentSaved] = useState(true)
  const [answers, setAnswers] = useState<Record<string,string>>({})
  const [nokComments, setNokComments] = useState<Record<string,string>>({})
  const [inspectionDecision, setInspectionDecision] = useState('')
  const [templateOverrides, setTemplateOverrides] = useState<Record<string,string>>({})
  const defaultTemplate = resolveInspectionTemplate(selectedEquipmentId)
  const templateCode = templateOverrides[selectedEquipmentId] ?? defaultTemplate.code
  const inspectionTemplate = templateCode === 'MEULEUSE' ? meuleuseTemplate : genericTemplate
  const inspectionPoints = inspectionTemplate?.sections.flatMap(section => section.points) ?? []
  const inspectionComplete = inspectionPoints.filter(point => point.required).every(point => Boolean(answers[point.id]))
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
</main> : page === 'equipment' ? <>    <main>
      <header><div><h1>{t('equipment')}</h1><p>{t('equipmentListSub')}</p></div><div className="topSelectors"><label>{t('entity')} <select defaultValue="VMA Sud"><option>VMA Sud</option><option>VMA Nord</option><option>BE Maintenance</option></select></label><div className="languages">{[{code:'fr',label:'Français'},{code:'nl',label:'Nederlands'},{code:'en',label:'English'},{code:'pl',label:'Polski'}].map(item=><button key={item.code} title={item.label} aria-label={item.label} className={i18n.language===item.code?'selected':''} onClick={()=>changeLanguage(item.code)}><LanguageFlag code={item.code}/></button>)}</div></div><div className="headerActions"><button className="scan">⌗ {t('scan')}</button><button className="add">+ {t('newEquipment')}</button></div></header>
      <section className="search"><span>⌕</span><input placeholder={t('search')}/></section>
      <section className="equipmentToolbar"><div className="filterGroup"><button className="filterActive">{t('all')} <b>1284</b></button><button>{t('toInspect')} <b>37</b></button><button>{t('quarantine')} <b>8</b></button><button>{t('lost')} <b>5</b></button></div><button className="filters">☷ {t('filters')}</button></section>
      <section className="panel equipmentPanel"><div className="equipmentTable">
        <div className="eqRow eqHead"><span>{t('number')}</span><span>{t('equipment')}</span><span>{t('category')}</span><span>{t('location')}</span><span>{t('complianceLabel')}</span><span>{t('nextInspection')}</span><span></span></div>
        {equipment.map(e=><div className="eqRow clickable" key={e.id} onClick={()=>{setSelectedEquipmentId(e.id);setPage('equipmentDetail')}}><span><b>{e.id}</b><small>{t('demoSerial')}</small></span><span><b>{t(`demo.${e.id}.name`)}</b><small>{t('demoBrand')}</small></span><span>{t('portableTool')}</span><span>{t(`demo.${e.id}.place`)}</span><span><i className={'pill '+e.tone}>{e.state==='À contrôler'?t('due'):e.state==='Conforme'?t('compliant'):e.state}</i></span><span>{e.control==='Échu'?t('expired'):e.control}</span><span className="arrow">›</span></div>)}
      </div><div className="tableFooter"><span>{t('showing', {shown:4,total:'1 284'})}</span><div><button disabled>‹</button><button className="pageActive">1</button><button>2</button><button>3</button><button>…</button><button>321</button><button>›</button></div></div></section>
    </main></> : page === 'equipmentDetail' ? <main>
      <header><div><button className="backLink" onClick={()=>setPage('equipment')}>← {t('backToEquipment')}</button><h1>{t(`demo.${selectedEquipment.id}.name`)}</h1><p>{selectedEquipment.id}</p></div><div className="topSelectors"><label>{t('entity')} <select defaultValue="VMA Sud"><option>VMA Sud</option><option>VMA Nord</option><option>BE Maintenance</option></select></label><div className="languages">{[{code:'fr',label:'Français'},{code:'nl',label:'Nederlands'},{code:'en',label:'English'},{code:'pl',label:'Polski'}].map(item=><button key={item.code} title={item.label} aria-label={item.label} className={i18n.language===item.code?'selected':''} onClick={()=>changeLanguage(item.code)}><LanguageFlag code={item.code}/></button>)}</div></div></header>
      <section className="detailStatus"><div><span className="equipmentBadge">{selectedEquipment.id}</span><i className="pill warning">{t('due')}</i></div><div className="detailActions"><button>⌗ {t('showQr')}</button><button>⇄ {t('moveEquipment')}</button><button className="add" onClick={()=>setPage('inspection')}>✓ {t('inspect')}</button></div></section>
      <section className="detailGrid">
        <div className="detailMain">
          <section className="panel"><div className="panelHead"><div><h2>{t('identification')}</h2><p>{t('identificationSub')}</p></div><button>{t('edit')}</button></div><div className="infoGrid">
            <div><small>{t('businessNumber')}</small><b>{selectedEquipment.id}</b></div><div><small>{t('serialNumber')}</small><b>GW18-2409138</b></div><div><small>{t('brand')}</small><b>Bosch Professional</b></div><div><small>{t('modelLabel')}</small><b>GWS 18V-10</b></div><div><small>{t('category')}</small><b>{t('portableTool')}</b></div><div><small>{t('organization')}</small><b>VMA Sud · HVAC</b></div>
          </div></section>
          <section className="panel"><div className="panelHead"><div><h2>{t('inspectionTracking')}</h2><p>{t('inspectionTrackingSub')}</p></div><button>{t('history')}</button></div><div className="templateAssignment"><label htmlFor="tooly-template-choice">Fiche de contrôle attribuée</label><select id="tooly-template-choice" className="detailSelect" value={templateOverrides[selectedEquipmentId] ?? 'AUTO'} onChange={event=>{const code=event.target.value;setTemplateOverrides(previous=>{const next={...previous};if(code==='AUTO')delete next[selectedEquipmentId];else next[selectedEquipmentId]=code;return next});setAnswers({});setNokComments({});setInspectionDecision('')}}><option value="AUTO">Automatique — {defaultTemplate.name}</option><option value="GENERIC">Contrôle générique</option><option value="MEULEUSE">Meuleuse</option></select><small>Modèle appliqué : {inspectionTemplate.name}. Modification valable pour les prochains contrôles (prototype local).</small></div>
            <div className="inspectionCards"><article><span className="statusDot warning"></span><div><small>{t('internalPeriodic')}</small><b>{t('dueOn')} 12/10/2026</b><p>{t('lastInspection')} 12/07/2026 · {t('compliant')}</p></div><button onClick={()=>setPage('inspection')}>✓ {t('inspect')}</button></article><article><span className="statusDot good"></span><div><small>{t('preUse')}</small><b>{t('inOrder')}</b><p>{t('verifiedOn')} 06/10/2026</p></div></article></div>
          </section>
          <section className="panel"><div className="panelHead"><div><h2>{t('recentHistory')}</h2><p>{t('recentHistorySub')}</p></div><button>{t('seeAll')} →</button></div><div className="timeline"><div><span>⇄</span><p><b>{t('assignedToWorksite')}</b><small>WTECEWA31 · 02/10/2026 · C. Comblé</small></p></div><div><span>✓</span><p><b>{t('periodicInspectionDone')}</b><small>12/07/2026 · {t('compliant')}</small></p></div><div><span>▣</span><p><b>{t('commissioned')}</b><small>15/03/2024 · Stock LLN</small></p></div></div></section>
        </div>
        <aside className="detailSide">
          <section className="panel locationCard"><h2>{t('currentLocation')}</h2><strong>{t('worksite')}</strong><select className="detailSelect" value={worksite} onChange={e=>{setWorksite(e.target.value);setAssignmentSaved(false)}}><option>WTECEWA31</option><option>WTECEWA42</option><option>Stock LLN</option><option>Atelier Jumet</option></select><small>{t('since')} 02/10/2026</small>
          <div className="holderBlock"><span>{t('assignedPerson')}</span><select className="detailSelect" value={holder} onChange={e=>{setHolder(e.target.value);setAssignmentSaved(false)}}><option>Marc Dupont</option><option>Jean Martin</option><option>Cédric Comblé</option><option>{t('unassigned')}</option></select></div>
          <button className={assignmentSaved?'savedAssignment':''} onClick={()=>setAssignmentSaved(true)}>⇄ {assignmentSaved?t('assignmentSaved'):t('confirmAssignment')}</button></section>
          <section className="panel"><h2>{t('documents')}</h2><div className="docList"><button>▤ <span>{t('safetySheet')}<small>PDF · v3</small></span>›</button><button>▤ <span>{t('userManual')}<small>PDF</small></span>›</button><button>▤ <span>{t('ceDeclaration')}<small>PDF</small></span>›</button></div><button className="secondaryFull">+ {t('addDocument')}</button></section>
          <section className="panel qrCard"><div className="fakeQr">TOOLY<br/><b>{selectedEquipment.id}</b></div><div><h2>{t('qrIdentification')}</h2><p>{t('qrInstalled')}</p><small>18/09/2026</small></div></section>
        </aside>
      </section>
    </main> : <main className="inspectionPage">
      <header><div><button className="backLink" onClick={()=>setPage('equipmentDetail')}>← {t('backToEquipmentRecord')}</button><h1>{t('fieldInspection')}</h1><p>{selectedEquipment.id} · {t(`demo.${selectedEquipment.id}.name`)}</p></div><div className="inspectionProgress"><b>{Object.keys(answers).length}/{inspectionPoints.length}</b><small>{t('pointsAnswered')}</small></div></header>
      <section className="fieldContext"><div><small>{t('currentWorksite')}</small><b>{worksite}</b></div><div><small>{t('assignedPerson')}</small><b>{holder}</b></div><button onClick={()=>setPage('equipmentDetail')}>{t('correctAssignment')}</button></section>
      <section className="panel inspectionIntro"><div><span className="equipmentBadge">VMA-0248</span><i className="pill warning">{t('periodicInspection')}</i></div><h2>{inspectionTemplate.title}</h2><p>{t('inspectionMobileHint')}</p>
        <details className="usageReminders"><summary>{t('beforeUseReminders')}</summary><ul>{inspectionTemplate.reminders.map(reminder=><li key={reminder}>{reminder}</li>)}</ul></details></section>
      <section className="checkpointList">
        {inspectionTemplate.sections.map(section=><section className="checkpointSection" key={section.title}><h2>{section.title}</h2>{section.points.map(point=>{const index=inspectionPoints.findIndex(item=>item.id===point.id)+1;return <article className={'checkpoint '+(answers[point.id]?'answered':'')} key={point.id}><div className="checkpointText"><span>{index}</span><div><b>{point.text}</b></div></div><div className="answerButtons">{['OK','NOK'].concat(point.allowsNa?['NA']:[]).map(value=><button key={value} className={answers[point.id]===value?('answerSelected '+value.toLowerCase()):''} onClick={()=>setAnswers({...answers,[point.id]:value})}>{value==='NA'?t('na'):value}</button>)}</div>{answers[point.id]==='NOK'&&<div className="nokDetail"><label>{t('nokComment')} *</label><textarea value={nokComments[point.id]||''} onChange={e=>setNokComments({...nokComments,[point.id]:e.target.value})} placeholder={t('nokCommentPlaceholder')}/></div>}</article>})}</section>)}
      </section>
      {Object.values(answers).includes('NOK') && <section className="panel nokDecision"><h2>{t('nokDecisionTitle')}</h2><p>{t('nokDecisionHelp')}</p><div className="decisionButtons"><button className={inspectionDecision==='NOK'?'selected':''} onClick={()=>setInspectionDecision('NOK')}>{t('keepNok')}</button><button className={inspectionDecision==='QUARANTINE'?'selected quarantineChoice':''} onClick={()=>setInspectionDecision('QUARANTINE')}>{t('putInQuarantine')}</button><button className={inspectionDecision==='DECOMMISSIONED'?'selected dangerChoice':''} onClick={()=>setInspectionDecision('DECOMMISSIONED')}>{t('decommission')}</button></div><label className="actionLabel">{t('correctiveAction')}</label><textarea placeholder={t('correctiveActionPlaceholder')}/></section>}
      <section className="inspectionFooter"><div><span>{t('inspectionResult')}</span><b>{Object.values(answers).includes('NOK')?(inspectionDecision==='QUARANTINE'?t('quarantineResult'):inspectionDecision==='DECOMMISSIONED'?t('decommissionedResult'):'NOK'):inspectionComplete?t('compliant'):t('inProgress')}</b></div><button disabled={!inspectionComplete || (Object.entries(answers).some(([id,v])=>v==='NOK' && !(nokComments[id]||'').trim())) || (Object.values(answers).includes('NOK') && !inspectionDecision)}>{t('finishInspection')}</button></section>
    </main>}
  </div>
}
export default App

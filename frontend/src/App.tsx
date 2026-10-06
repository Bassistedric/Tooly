const equipment = [
  { id:'VMA-0248', name:'Meuleuse angulaire', place:'Chantier WTECEWA31', control:'12/10/2026', state:'À contrôler', tone:'warning' },
  { id:'VMA-0314', name:'Marteau-piqueur', place:'Camionnette 2-ABC-123', control:'28/11/2026', state:'Conforme', tone:'ok' },
  { id:'VMA-0187', name:'Manomètre digital', place:'Atelier LLN', control:'Échu', state:'NOK', tone:'danger' },
  { id:'VMA-0421', name:'Perceuse-visseuse', place:'Stock Jumet', control:'15/01/2027', state:'Conforme', tone:'ok' },
]

function App() {
  return <div className="shell">
    <aside>
      <div className="brand"><span className="brandMark">T</span><div><b>Tooly</b><small>Equipment management</small></div></div>
      <nav>
        <button className="active">⌂ <span>Tableau de bord</span></button>
        <button>▣ <span>Équipements</span></button>
        <button>⌖ <span>Chantiers</span></button>
        <button>✓ <span>Contrôles</span><em>12</em></button>
        <button>⇄ <span>Mouvements</span></button>
        <button>▤ <span>Documents</span></button>
        <button>◇ <span>Produits / FDS</span></button>
      </nav>
      <div className="asideBottom"><button>⚙ <span>Administration</span></button><div className="profile"><span>CC</span><div><b>Cédric C.</b><small>Administrateur</small></div></div></div>
    </aside>
    <main>
      <header><div><h1>Bonjour Cédric</h1><p>Vue d'ensemble du parc matériel</p></div><div className="headerActions"><button className="scan">⌗ Scanner</button><button className="add">+ Nouvel équipement</button></div></header>
      <section className="search"><span>⌕</span><input placeholder="Rechercher un n° VMA, série, appareil, personne, camionnette, chantier…"/></section>
      <section className="metrics">
        <article><span className="metricIcon">▣</span><div><small>ÉQUIPEMENTS ACTIFS</small><strong>1 284</strong><p>+ 18 ce mois</p></div></article>
        <article><span className="metricIcon warn">◷</span><div><small>À CONTRÔLER</small><strong>37</strong><p>12 dans les 7 jours</p></div></article>
        <article><span className="metricIcon danger">!</span><div><small>NOK / QUARANTAINE</small><strong>8</strong><p>3 actions en attente</p></div></article>
        <article><span className="metricIcon good">✓</span><div><small>CONFORMITÉ DU PARC</small><strong>96,8 %</strong><p>1 239 en ordre</p></div></article>
      </section>
      <section className="contentGrid">
        <div className="panel wide"><div className="panelHead"><div><h2>Équipements à suivre</h2><p>Échéances et anomalies prioritaires</p></div><button>Voir tout →</button></div>
          <div className="table"><div className="tr th"><span>ÉQUIPEMENT</span><span>LOCALISATION</span><span>PROCHAIN CONTRÔLE</span><span>STATUT</span><span></span></div>
          {equipment.map(e=><div className="tr" key={e.id}><span><b>{e.name}</b><small>{e.id}</small></span><span>{e.place}</span><span>{e.control}</span><span><i className={'pill '+e.tone}>{e.state}</i></span><span className="arrow">›</span></div>)}</div>
        </div>
        <div className="panel"><div className="panelHead"><div><h2>Contrôles</h2><p>30 prochains jours</p></div></div>
          <div className="ring"><div><strong>37</strong><small>à traiter</small></div></div>
          <div className="legend"><p><i className="dot danger"></i><span>Échus</span><b>9</b></p><p><i className="dot warning"></i><span>≤ 7 jours</span><b>12</b></p><p><i className="dot"></i><span>8–30 jours</span><b>16</b></p></div>
          <button className="primaryFull">Ouvrir la tournée de contrôle</button>
        </div>
      </section>
      <section className="panel quick"><div><h2>Accès rapide</h2><p>Actions terrain les plus utilisées</p></div><div className="quickActions"><button><b>⌗</b><span>Identifier un appareil<small>QR ou numéro</small></span></button><button><b>✓</b><span>Effectuer un contrôle<small>Fiche adaptée automatiquement</small></span></button><button><b>⇄</b><span>Affecter / déplacer<small>Chantier, véhicule, stock…</small></span></button><button><b>▤</b><span>Ouvrir une FDS<small>Recherche produit</small></span></button></div></section>
    </main>
  </div>
}
export default App

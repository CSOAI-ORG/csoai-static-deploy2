// THE canonical sovereign node graph — one source of truth every surface reads:
// the dock globe avatar, the MEOK Earth world (world.meok.ai), the force-graph, the
// browser extension. Add a node here and it lights up everywhere. CORS-open so any
// origin (incl. world.meok.ai) can fetch it.
//
// Grounded in the real MEOK estate: the legacy-bridge family + framework temples are
// placed across global hubs. Roles are the bridge/governance categories anchored at
// each city; status is the flywheel posture (governed = signed & adjudicated).

const NODES = [
  { id: 'london',    name: 'London',    lat: 51.5,  lon: -0.1,  status: 'governed', role: 'HQ · COBOL · ISO 20022 · CICS', kind: 'hq' },
  { id: 'newyork',   name: 'New York',  lat: 40.7,  lon: -74.0, status: 'governed', role: 'FIX · NACHA · ISO 8583 (trading & payments)', kind: 'finance' },
  { id: 'frankfurt', name: 'Frankfurt', lat: 50.1,  lon: 8.7,   status: 'governed', role: 'SAP · ACORD (enterprise & insurance)', kind: 'enterprise' },
  { id: 'tokyo',     name: 'Tokyo',     lat: 35.7,  lon: 139.7, status: 'governed', role: 'AS/400 · MQTT (manufacturing & IoT)', kind: 'industrial' },
  { id: 'singapore', name: 'Singapore', lat: 1.35,  lon: 103.8, status: 'governed', role: 'EDI · GS1 (trade & supply chain)', kind: 'trade' },
  { id: 'mumbai',    name: 'Mumbai',    lat: 19.1,  lon: 72.9,  status: 'governed', role: 'Oracle · tax bridges', kind: 'finance' },
  { id: 'dubai',     name: 'Dubai',     lat: 25.2,  lon: 55.3,  status: 'watch',    role: 'logistics & trade corridor', kind: 'trade' },
  { id: 'saopaulo',  name: 'São Paulo', lat: -23.5, lon: -46.6, status: 'governed', role: 'payments · NACHA-equiv', kind: 'finance' },
  { id: 'sydney',    name: 'Sydney',    lat: -33.9, lon: 151.2, status: 'governed', role: 'SCADA · DLMS (energy & utilities)', kind: 'industrial' },
  { id: 'toronto',   name: 'Toronto',   lat: 43.7,  lon: -79.4, status: 'governed', role: 'MISMO (mortgage) · insurance', kind: 'enterprise' },
  { id: 'hongkong',  name: 'Hong Kong', lat: 22.3,  lon: 114.2, status: 'governed', role: 'FIX · markets', kind: 'finance' },
  { id: 'capetown',  name: 'Cape Town', lat: -33.9, lon: 18.4,  status: 'watch',    role: 'HL7/FHIR health bridge (emerging)', kind: 'health' },
];

// the connector arcs (legacy → governed core)
const LINKS = [
  ['london', 'newyork'], ['london', 'frankfurt'], ['newyork', 'toronto'], ['newyork', 'saopaulo'],
  ['frankfurt', 'dubai'], ['singapore', 'tokyo'], ['singapore', 'hongkong'], ['mumbai', 'dubai'],
  ['tokyo', 'sydney'], ['london', 'capetown'], ['hongkong', 'tokyo'],
];

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'public, max-age=300');
  if (req.method === 'OPTIONS') return res.status(204).end();
  return res.status(200).json({
    version: '1.0',
    source: 'os.meok.ai/api/nodes — canonical sovereign node graph',
    legend: { governed: 'signed & council-adjudicated', watch: 'monitored', flagged: 'action required' },
    count: NODES.length,
    nodes: NODES,
    links: LINKS,
  });
}

const fetch = require('node-fetch');

module.exports = async function handler(req, res) {
    try {
        const apiUrl = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid';
        const proxyApiKey = process.env.PROXY_API_KEY; 
        const serviceKey = process.env.SEOUL_BUS_API_KEY; 
        const arsId = req.query.arsId;

        const proxyUrl = `https://proxy.scrapeops.io/v1/?api_key=${proxyApiKey}&url=${encodeURIComponent(`${apiUrl}?serviceKey=${serviceKey}&arsId=${arsId}`)}`;

        console.log("Fetching via Proxy:", proxyUrl);

        const response = await fetch(proxyUrl);
        if (!response.ok) throw new Error('프록시 서버 응답 실패');

        const data = await response.text();
        res.setHeader('Access-Control-Allow-Origin', '*'); // CORS 해결
        res.status(200).send(data);

    } catch (error) {
        console.error('Error fetching API:', error);
        res.status(500).json({ error: error.message });
    }
};

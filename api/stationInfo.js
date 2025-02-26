module.exports = async function handler(req, res) {
    try {
        const apiUrl = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid';
        const serviceKey = process.env.SEOUL_BUS_API_KEY;
        const arsId = req.query.arsId;

        const response = await fetch(`${apiUrl}?serviceKey=${encodeURIComponent(serviceKey)}&arsId=${arsId}`);
        if (!response.ok) throw new Error('Failed to fetch data from external API');

        const data = await response.text();

        // CORS 허용 헤더 설정
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(data);

    } catch (error) {
        console.error('Error fetching API:', error);
        res.status(500).json({ error: error.message });
    }
};

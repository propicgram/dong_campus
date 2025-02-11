let cacheData = null;
let cacheTimestamp = 0;

module.exports = async function handler(req, res) {
    const now = Date.now();
    const forceUpdate = req.query.forceUpdate === 'true';  // 쿼리 파라미터로 강제 업데이트 판단

    // 캐시 무효화 조건
    if (!forceUpdate && cacheData && now - cacheTimestamp < 30000) {
        console.log('Serving cached data');
        res.setHeader('Cache-Control', 'public, max-age=30');
        return res.status(200).send(cacheData);
    }

    try {
        const apiUrl = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid';
        const serviceKey = process.env.SEOUL_BUS_API_KEY;
        const arsId = req.query.arsId || '12121';

        const response = await fetch(`${apiUrl}?serviceKey=${encodeURIComponent(serviceKey)}&arsId=${arsId}`);
        if (!response.ok) throw new Error('Failed to fetch data from external API');

        const data = await response.text();

        // 새로운 캐시 저장
        cacheData = data;
        cacheTimestamp = now;

        // 클라이언트 캐시 설정 (30초 캐시)
        res.setHeader('Cache-Control', 'public, max-age=30');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(data);

    } catch (error) {
        console.error('Error fetching API:', error);
        res.status(500).json({ error: error.message });
    }
};

import {useState, useEffect, useRef} from "react";
import Single from "./ChartjsSingle.jsx";


/**
 *
 */
export default function App() {
    const [charts, setCharts] = useState(window.charts || []);

    return (
        <div className={"flex flex-col space-y-8 [&>div]:py-8 [&>div+div]:border-t [&>div+div]:border-slate-300"}>
            {charts.map(chart => <Single definition={chart} />)}
        </div>
    )
}
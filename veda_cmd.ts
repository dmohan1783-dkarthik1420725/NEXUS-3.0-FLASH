import { GoogleGenerativeAI } from "@google/generative-ai";
import OpenAI from "openai";
import { DDGS } from "ddgs";

// --- SOVEREIGN CORE ---
const genAI = new GoogleGenerativeAI("YOUR_GEMINI_KEY");
const ghost_mesh = new OpenAI({
    apiKey: "YOUR_POLLINATIONS_KEY",
    baseURL: "https://gen.pollinations.ai/v1"
});

async function vedaDeepDive() {
    const query = process.argv.slice(2).join(" ");
    if (!query) return console.log("🔱 VEDA 3.1 ULTRA: COMMANDER, SPECIFY THE TARGET.");

    console.log("🔱 INITIATING DEEP SCOUT...");

    try {
        // 1. EXTRACT ALL WEB DATA (The Scouter)
        const ddgs = new DDGS();
        const searchResults = await ddgs.text(query, { max_results: 8 });
        
        let rawWebData = "";
        console.log("\n--- RAW WEB SOURCES DETECTED ---");
        searchResults.forEach((res, i) => {
            console.log(`[${i+1}] SOURCE: ${res.href}`);
            rawWebData += `\nSOURCE [${i+1}]: ${res.title}\nCONTENT: ${res.body}\nURL: ${res.href}\n`;
        });

        // 2. BRAIN 1: GEMINI PRO (DATA ANALYSIS)
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
        const geminiRes = await model.generateContent(`
            SYSTEM: Extract all key data points from these web pages. Do not summarize. 
            WEB PAGES DATA: ${rawWebData}
            COMMANDER'S QUERY: ${query}
        `);

        // 3. BRAIN 2: OPENAI/GHOST (REFINEMENT & VERIFICATION)
        const finalRefined = await ghost_mesh.chat.completions.create({
            model: "openai",
            messages: [
                { role: "system", content: "You are VEDA 3.1 ULTRA. Format the following data into an elite technical report. Include all URLs and specific facts." },
                { role: "user", content: geminiRes.response.text() }
            ]
        });

        console.log("\n--- SOVEREIGN INTEL REPORT ---");
        console.log(finalRefined.choices[0].message.content);
        console.log("\n--- END OF TRANSMISSION ---");

    } catch (error) {
        console.error("🔱 CRITICAL ERROR IN NEURAL CORRIDORS:", error);
    }
}

vedaDeepDive();
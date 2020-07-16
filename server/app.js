const express = require('express')
const cors = require('cors')
const path = require('path')
const app = express()
const port = 3000

app.use(cors())
app.use(express.json())

const executeProgramPython = (name, params = []) => {
    const { spawn } = require('child_process')
    const program = path.join(__dirname, `script/${name}.py`)
    return spawn('python3', [program, ...params])
}

app.post('/api/exec/register', (req, res) => {
    const {
        name,
        lastname
    } = req.body;

    res.send({
        msg: 'The program start in seconds'
    })

    const programPython = executeProgramPython('register', [name, lastname])

    programPython.stdout.on('data', (data) => {
        console.log(data.toString())
    })

    programPython.on('close', (code) => {
        console.log(`python program exit with code ${code}`)
    })
})

app.post('/api/exec/recognize', (req, res) => {
    const {
        name,
        lastname
    } = req.body;

    res.send({
        msg: 'The program start in seconds'
    })

    const programPython = executeProgramPython('recognize', [name, lastname])

    programPython.stdout.on('data', (data) => {
        console.log(data.toString())
    })

    programPython.on('close', (code) => {
        console.log(`python program exit with code ${code}`)
    })
})

app.listen(port, () => {
    console.log(`server run on port ${port}`)
})

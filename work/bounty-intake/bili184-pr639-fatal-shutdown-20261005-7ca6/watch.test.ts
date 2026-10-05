import { Bundler } from '../src'
import logger from '../src/logger'
import { watch } from 'rollup'

jest.mock('rollup', () => ({
  rollup: jest.fn(),
  watch: jest.fn(),
}))

const mockWatch = watch as jest.Mock

function createBundler() {
  return new Bundler(
    { input: 'index.js' },
    {
      configFile: false,
      logLevel: 'quiet',
      rootDir: __dirname,
    }
  )
}

describe('watch mode', () => {
  beforeEach(() => {
    mockWatch.mockReset()
    jest.spyOn(logger, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('closes once when Rollup emits repeated fatal events', async () => {
    const error = new Error('watch failed')
    const close = jest.fn()
    let onEvent: ((payload: any) => void) | undefined

    mockWatch.mockReturnValue({
      close,
      on(_event: string, listener: (payload: any) => void) {
        onEvent = listener
      },
    })

    await createBundler().run({ watch: true })
    onEvent!({ code: 'FATAL', error })
    onEvent!({ code: 'FATAL', error })

    expect(logger.error).toHaveBeenCalledWith('watch failed')
    expect(close).toHaveBeenCalledTimes(1)
  })

  it('reports watcher-close failures after the fatal diagnostic', async () => {
    const error = new Error('watch failed')
    const closeError = new Error('close failed')
    const close = jest.fn().mockRejectedValue(closeError)
    let onEvent: ((payload: any) => void) | undefined

    mockWatch.mockReturnValue({
      close,
      on(_event: string, listener: (payload: any) => void) {
        onEvent = listener
      },
    })

    await createBundler().run({ watch: true })
    onEvent!({ code: 'FATAL', error })
    await new Promise((resolve) => setImmediate(resolve))

    expect(logger.error).toHaveBeenNthCalledWith(1, 'watch failed')
    expect(logger.error).toHaveBeenNthCalledWith(2, 'close failed')
  })

  it('keeps logging normal Rollup watch errors', async () => {
    const error = new Error('build failed')

    mockWatch.mockReturnValue({
      on(_event: string, listener: (payload: any) => void) {
        listener({ code: 'ERROR', error })
      },
    })

    await createBundler().run({ watch: true })

    expect(logger.error).toHaveBeenCalledWith('build failed')
  })

  it('ignores non-error watch events', async () => {
    mockWatch.mockReturnValue({
      on(_event: string, listener: (payload: any) => void) {
        listener({ code: 'BUNDLE_END' })
      },
    })

    await createBundler().run({ watch: true })

    expect(logger.error).not.toHaveBeenCalled()
  })
})

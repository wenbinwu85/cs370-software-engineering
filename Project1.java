import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;


public class Project1 {
    public static void main(String[] args) {
        int numThreads = 1000;
        int n = 100; // # of spins
        double B = 0.0;
        double C = -1.0;
        double T = 1.9;

        System.out.println("Calculating <m> and <cp>...");

        // spawn the threads
        ArrayList<SpinThread> metropolisThreads = new ArrayList<>();
        for (int i = 0; i < numThreads; i++) {
            metropolisThreads.add(new SpinThread(n, B, C, T));
            metropolisThreads.get(i).start();
        }

        // join
        for (int i = 0; i < numThreads; i++) {
            try {
                if (metropolisThreads.get(i).isAlive()) {
                    metropolisThreads.get(i).join();
                }
            } catch (Exception e) {
            }
        }

        /*
        -----  this code used to get good Nm and Nf values -----

        // calculate cp theory value using equation 1.8.2
        double top = Math.exp(C / T) - Math.exp(-C / T);
        double bottom = Math.exp(C / T) + Math.exp(-C / T);
        double cpTheory = top / bottom; // -0.4825598285864788

        // calculate relative error using equation 1.9.1
        double cpMeanSum = 0;
        for (int i = 0; i < numThreads; i++) {
            SpinThread st = metropolisThreads.get(i);
            double cpMean = st.cpSum / SpinThread.Nm; // c[j] = cpSum / Nm , equation 1.7.2a
            cpMeanSum += (cpMean - cpTheory) / cpTheory;
        }
        double relativeError = cpMeanSum / numThreads;

        // calculate variance value using quation 1.9.2
        cpMeanSum = 0;
        for (int i = 0; i < numThreads; i++) {
            SpinThread st = metropolisThreads.get(i);
            double cpMean = st.cpSum / SpinThread.Nm; // c[j] = cpSum / Nm , equation 1.7.2a
            cpMeanSum += Math.pow((cpMean - cpTheory) / cpTheory - relativeError, 2);
        }
        double variance = cpMeanSum / numThreads;

        System.out.println("rc: " + relativeError);
        System.out.println("va: " + variance + "\n");

        --------------------------------------------------------
        */

        // calculate the mean of <m> and <cp>
        ArrayList<Double> mMeanArray = new ArrayList<>(); // m[j] array
        ArrayList<Double> cpMeanArray = new ArrayList<>(); // cp[j] array
        double mMeanSum = 0; // sum of all m[j]
        double cpMeanSum = 0; // sum of all cp[j]
        for (int i = 0; i < numThreads; i++) {
            SpinThread st = metropolisThreads.get(i);
            double mMean = st.mSum / SpinThread.Nm; // m[j]
            double cpMean = st.cpSum / SpinThread.Nm; // cp[j]
            mMeanArray.add(mMean);
            cpMeanArray.add(cpMean);
            mMeanSum += mMean;
            cpMeanSum += cpMean;
        }
        // calcualte global mean for <m> and <cp>
        double mGlobalMean = mMeanSum / numThreads;
        double cpGlobalMean = cpMeanSum / numThreads;

        System.out.println(T + "     " + mGlobalMean + "     " + cpGlobalMean);
    }
}


class SpinThread extends Thread {
    // Nm = 3 Nf = 470
    public static int Nm = 3; // relative error = 0.01934165298051108
    public static int Nf = 470; // variance = 0.011412163711925483

    public int n = 0;
    public double B = 0;
    public double C = 0;
    public double T = 0;
    public double mSum;
    public double cpSum;
    public ArrayList<Double> mArray = new ArrayList<>();
    public ArrayList<Double> cpArray = new ArrayList<>();

    SpinThread(int n, double b, double c, double t) {
        this.n = n;
        this.B = b;
        this.C = c;
        this.T = t;
    }

    @Override
    public void run() {
        // call the metropolis algorithm Nm times
        for (int i = 0; i < Nm; i++) {
            ArrayList<Integer> optConfig = metropolis(n, B, C, T);
            double m = magnetization(optConfig);
            double cp = pairCorrelation(optConfig);

            mArray.add(m);
            cpArray.add(cp);
            mSum += m;
            cpSum += cp;
        }
    }

    public static double magnetization(ArrayList<Integer> spinConfig) {
        double sum = 0;
        for (int i = 0; i < spinConfig.size(); i++) {
            sum += spinConfig.get(i);
        }
        double magnetization = sum / spinConfig.size();
        return magnetization;
    }

    public static double pairCorrelation(ArrayList<Integer> spinConfig) {
        double sum = 0;
        for (int i = 0; i < (spinConfig.size() - 1); i++) {
            sum += spinConfig.get(i) * spinConfig.get(i + 1);
        }
        sum += spinConfig.get(spinConfig.size() - 1) * spinConfig.get(0);
        double cp = sum / spinConfig.size();
        return cp;
    }

    public static double energy(ArrayList<Integer> spinConfig, double B, double C) {
        double sum = 0;
        for (int i = 0; i < spinConfig.size() - 1; i++) {
            sum += spinConfig.get(i) * (B + C * spinConfig.get(i + 1));
        }
        sum += spinConfig.get(spinConfig.size() - 1) * (B + C * spinConfig.get(0));
        double energy = -1 * sum;
        return energy;
    }

    public static ArrayList<Integer> metropolis(int n, double B, double C, double T) {
        ArrayList<Integer> currentConfig = new ArrayList<>();
        // setup spins configuration 0
        if (C >= 0) {
            for (int i = 0; i < n; i++) {
                currentConfig.add(1);
            }
        } else {
            for (int i = 0; i < n; i++) {
                currentConfig.add(i, (int) Math.pow(-1, i));
            }
        }

        int flips = n * Nf;
        for (int i = 0; i < flips; i++) {
            ArrayList<Integer> newConfig = new ArrayList<>(currentConfig);

            int randomSpin = ThreadLocalRandom.current().nextInt(n);
            int flipValue = (newConfig.get(randomSpin) == 1) ? -1 : 1;
            newConfig.set(randomSpin, flipValue);

            // can be calculated without computing E(σ1) and E(σ0) separately!!!!!!!
            double currentConfigEnergy = energy(currentConfig, B, C);
            double newConfigEnergy = energy(newConfig, B, C);
            double energyDelta = newConfigEnergy - currentConfigEnergy;

            if (energyDelta < 0) {
                currentConfig = new ArrayList<>(newConfig);
            } else if (energyDelta > 0) {
                double p = Math.exp((-1 * energyDelta) / T);
                double r = ThreadLocalRandom.current().nextDouble();
                if (r < p) {
                    currentConfig = new ArrayList<>(newConfig);
                }
            }
        }
        return currentConfig;
    }
}